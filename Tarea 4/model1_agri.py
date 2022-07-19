    #Setup preamble

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing



mainpath = "/Users/malenahedemann/Desktop/Clases herramientas/Clase 4"
suit = "{}/SUIT/suit/hdr.adf".format(mainpath)
gadm = "{}/gadm41_USA_shp/gadm41_USA_2.shp".format(mainpath)
outpath = "{}/_output/counties_agrisuit.csv".format(mainpath)
junkpath = "{}/_output/junk".format(mainpath)
junkfile = "{}/_output/junk/agrisuit.tif".format(mainpath)
if not os.path.exists(mainpath + "/_output"):
    os.mkdir(mainpath + "/_output")
if not os.path.exists(junkpath):
    os.mkdir(junkpath)
    
    
###################################################################
    #we create the model
class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Agrisuit', 'agrisuit', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Counties', 'counties', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonal', 'Zonal', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}
###################################################################
        # Drop field(s)
###################################################################
#We eliminate certain variables that won't be used
        alg_params = {
                    'COLUMN':
            ['GID_0','NAME_0','GID_1',
             'GID_2','HASC_2','CC_2',
             'TYPE_2','NL_NAME 2','VARNAME_2',
             'NL_NAME_1','NL_NAME_2',' ENGTYPE_2'],
            'INPUT': 'gadm',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
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
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Agrisuit']
        }
        Agrisuit = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Add autoincremental field
###################################################################
        alg_params = {
            'FIELD_NAME': 'cid',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['DropFields']['OUTPUT'],
            'MODULUS': None,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Counties']
        }
        cpunties = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Zonal statistics
###################################################################
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'INPUT_RASTER': outputs['WarpReproject']['OUTPUT'],
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Zonal']
        }
      processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)


    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
