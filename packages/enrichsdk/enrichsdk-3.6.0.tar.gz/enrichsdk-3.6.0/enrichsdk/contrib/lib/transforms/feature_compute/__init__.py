import os
import json
import logging
from collections import defaultdict
from datetime import datetime, date, timedelta
from dateutil import parser as dateparser
import pandas as pd

from enrichsdk import Compute, S3Mixin, CheckpointMixin

logger = logging.getLogger("app")

__all__ = ['FeaturesetExtractorBase',
           'FeatureExtractorBase',
           'FeatureComputeBase',
           'note']

def note(df, title):
    msg = title + "\n"
    msg += "--------" + "\n"
    msg += "Timestamp: " + str(datetime.now()) + "\n"
    msg += "\nShape: "+ str(df.shape) + "\n"
    msg += "\nColumns: " + ", ".join(df.columns) + "\n"
    if len(df) > 0:
        msg += "\nSample:" + "\n"
        msg += df.sample(min(2, len(df))).T.to_string() + "\n" + "\n"
    msg += "\nDtypes" + "\n"
    msg += df.dtypes.to_string() + "\n"
    msg += "------" + "\n"
    return msg

class FeatureExtractorBase:
    """
    Simple baseclass
    """
    def extract(self, name, data, key=None):
        """
        Given data and a name, generate some attributes. The
        return value should be a list of dictionaries
        """
        raise Exception("Not implemented")


class FeaturesetExtractorBase:
    """
    Compute one featureset. To be used in conjunction with the
    feature compute class. We define multiple extractors
    """

    def get_extractors(self):
        """
        Returns a list of extractors. This is over-ridden in
        the subclass
        """
        return []

    def get_specs(self):
        """
        Returns a list of specifications. Each specification applies to
        one dataset. It is possible to generate multiple featuresets
        from the same dataset

        For example::

            [
                {
                    "keys": ['age', 'sex'],
                    "extractor": "simple",
                }
            ]
            """
        return []

    def one_record(self, data):
        """
        Process one record at a time. Pass it through the
        extractors, collect the outputs and return

        """
        allfeatures = []

        extractors = self.get_extractors()
        specs = self.get_specs()
        for spec in specs:

            extractor = spec.get('extractor', 'default')
            extractor = extractors[extractor]

            if isinstance(spec['keys'], list):
                for key in spec['keys']:
                    if key not in data:
                        continue
                    features = extractor.extract(key, data)
                    allfeatures.extend(features)
            elif isinstance(spec['keys'], dict):
                for name, key in spec['keys'].items():
                    features = extractor.extract(name, data, key)
                    allfeatures.extend(features)

        return allfeatures

    def collate(self, features):
        """
        Combine a outputs of the extractors (each of which is a dictionary)
        into an object. It could be anything that the cleaner can handle.
        """
        return pd.DataFrame(features)

    def clean(self, df):
        """
        Clean the combined object (dataframe, list, other)
        """
        return df

    def finalize(self, df, computed):
        """
        Take cleaneddata and generate a final object such as a dataframe
        """
        return df

    def document(self, name, df):
        """
        Document the dataframe generated. The default is
        to capture schema, size etc. Over-ride to extend this
        documentation.
        """
        if not isinstance(df, pd.DataFrame):
            logger.error("Unable to document. Unsupported data format. Override method in subclass")
        else:
            return note(df, getattr(self, 'name', self.__class__.__name__))

class FeatureComputeBase(Compute):
    """
    A built-in transform baseclass to handle standard feature
    computation and reduce the duplication of code.

    This should be used in conjunction with an extractor
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "FeatureComputeBase"
        self._environ = os.environ.copy()

    @classmethod
    def instantiable(cls):
        """
        Return true if class can be instantiated
        """
        return False

    def get_featureset_extractors(self):
        """
        Return a list extractors. For example::

            {
                 "name": "patient",
                 "extractor": <instance>
            }
        """
        raise Exception("Implement in subclass")

    def store(self, data):
        raise Exception("Implement in subclass")

    def get_objects(self):
        """
        Get a list of objects (typically names)  to process
        """
        if 'root' not in args:
            raise Exception("Base class implementation required 'root'")

        root = self.args['root']
        files = os.listdir(root)
        return files

    def read_object(self, obj):
        """
        Read one object
        """

        if 'root' not in args:
            raise Exception("Base class implementation required 'root'")

        root = self.args['root']
        filename = os.path.join(root, obj)
        data = json.load(open(filename))
        return data

    def process(self, state):
        """
        Run the computation and update the state
        """

        logger.debug("Start execution",
                     extra=self.config.get_extra({
                         'transform': self.name
                     }))

        self.state = state

        # What extractors to run on the data..
        featureset_extractors = self.get_featureset_extractors()
        featureset_extractors = [f for f in featureset_extractors if f.get('enable', True)]

        featuresets = defaultdict(list)

        # Go through all the available objects
        objects = self.get_objects()
        logger.debug(f"Received {len(objects)} objects",
                     extra={
                         'transform': self.name
                     })

        counts = defaultdict(int)
        invalid_objects = []

        for obj in objects:
            try:
                counts['obj_total'] += 1
                try:
                    data = self.read_object(obj)
                    if not isinstance(data, (dict, list)):
                        counts['object_read_invalid'] += 1
                        invalid_objects.append(obj)
                        continue
                    if isinstance(data, dict):
                        data = [data]
                except Exception as e:
                    invalid_objects.append(str(obj) + ": " + str(e))
                    counts['objects_error'] += 1
                    continue

                for index, d in enumerate(data):
                    try:
                        counts['records_total'] += 1
                        if ((not isinstance(d, dict)) or (len(d) == 0)):
                            logger.error("Empty or invalid data",
                                         extra={
                                             'transform': self.name,
                                             'data': str(obj) + "\n" + str(d)[:100]
                                         })
                            counts['records_error_invalid'] += 1
                            continue

                        # Compute various feature sets for each patient
                        for detail in featureset_extractors:
                            try:
                                extractor = detail['extractor']
                                name       = detail['name']

                                # Process one record...
                                features = extractor.one_record(d)

                                # Skip if no features are being generated
                                if features is None:
                                    continue

                                if isinstance(features, dict):
                                    features = [features]
                                featuresets[name].extend(features)
                            except:
                                counts[f'extractor_{name}_exception'] += 1
                                if counts[f'extractor_{name}_exception'] == 1:
                                    logger.exception(f"Unable to process:{name}",
                                                     extra={
                                                         'transform': self.name,
                                                         'data': str(d)[:200]
                                                     })
                    except:
                        # Handle exceptions in individual records
                        counts['records_error_exception'] += 1
                        logger.exception(f"Error in processing {index}",
                                         extra={
                                             'transform': self.name,
                                             'data': str(obj) + "\n" + str(d)[:200]
                                         })

                counts['objects_valid'] += 1
            except:
                # Handle exceptions in individual records
                counts['objects_error_exception'] += 1
                logger.exception(f"Error in processing object",
                                         extra={
                                             'transform': self.name,
                                             'data': f"{obj}\n" + json.dumps(counts, indent=4)
                                         })

        logger.debug("Completed reading objects",
                     extra={
                         'transform': self.name,
                         'data': json.dumps(counts, indent=4) + "\nInvalid Objects:\n" + "\n".join(invalid_objects)
                     })

        # Now collect all features of all patient
        counts = defaultdict(int)
        computed = {}
        for detail in featureset_extractors:

            name = detail['name']
            extractor = detail['extractor']

            if ((name not in featuresets) or
                (featuresets[name] is None)):
                logger.warning(f"Features missing: {name}",
                             extra={
                                 'transform': self.name
                             })
                continue

            # Collect all the features into a dataframe..
            df = extractor.collate(featuresets[name])

            # Clean the dataframe generated.
            df = extractor.clean(df)

            computed[name] = df
            counts[name] = df.shape[0]

        logger.debug("Completed collating",
                     extra={
                         'transform': self.name,
                         'data': "records: " + json.dumps(counts, indent=4)
                     })

        # Now we have individual dataframes. May be the extractor
        # wants to compute some more.
        final = {}
        counts = defaultdict(int)
        for detail in featureset_extractors:
            name = detail['name']
            extractor = detail['extractor']
            df = computed.get(name, None)
            df = extractor.finalize(df, computed)
            if df is None:
                logger.error(f"{name}: Invalid result",
                             extra={
                                 'transform': self.name,
                             })
                continue
            final[name] = df
            counts[name] = df.shape[0]

        logger.debug("Completed finalization",
                     extra={
                         'transform': self.name,
                         'data': "records: " + json.dumps(counts, indent=4)
                     })

        # document...
        for detail in featureset_extractors:
            name = detail['name']
            extractor = detail['extractor']
            df = final[name]
            logger.debug(f"Featureset: {name}_features",
                         extra={
                             'transform': self.name,
                             "data": extractor.document(name, df)
                         })

            if isinstance(df, pd.DataFrame):
                self.update_frame(name + "_features",
                                  "Features computed over the available data",
                                  df, objects[0])

        # Store the result...
        self.store(final)

        logger.debug("Complete execution",
                     extra=self.config.get_extra({
                         'transform': self.name
                     }))

        ###########################################
        # => Return
        ###########################################
        return state

    def validate_results(self, what, state):
        """
        Check to make sure that the execution completed correctly
        """
        pass
