

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing

mainpath = "/Users/malenahedemann/Desktop/Clases herramientas/Clase 4"
suit = "{}/SUIT/suit/hdr.adf".format(mainpath)
    
###################################################################
    #we create the model

class Model2(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}
###################################################################
        # Warp (reproject)
###################################################################
        alg_params = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': 'suit',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Nearest Neighbour
            'SOURCE_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }
        Suitout = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
###################################################################
        # Extract projection
###################################################################
        alg_params = {
            'INPUT': outputs['WarpReproject']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        outputs['ExtractProjection'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model2'

    def displayName(self):
        return 'model2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model2()
