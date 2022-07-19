
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

mainpath = "/Users/malenahedemann/Desktop/Clases herramientas/Clase 4"
clean = "{}/Clean/clean.shp".format(mainpath)
admin = "{}/ne_10m_admin_0_countries/ ne_10m_admin_0_countries.shp".format(mainpath)
outpath = "{}/_output/counties_agrisuit.csv".format(mainpath)
junkpath = "{}/_output/junk".format(mainpath)
junkfile = "{}/_output/junk/agrisuit.tif".format(mainpath)
if not os.path.exists(mainpath + "/_output"):
    os.mkdir(mainpath + "/_output")
if not os.path.exists(junkpath):
    os.mkdir(junkpath)
    
###################################################################
    #we create the model
    
class Model4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixge_countries', 'fixge_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}
###################################################################
        # Fix geometries - wlds
###################################################################
        alg_params = {
            'INPUT': 'clean',
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        Fixgeo_wlds = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Fix geometries - countries
###################################################################
        alg_params = {
            'INPUT': 'admin',
            'OUTPUT': parameters['Fixge_countries']
        }
        Fixge_countries = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Statistics by categories
###################################################################
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': 'Intersection_3a806d6c_3247_4802_b4a9_d816c7b2f5bd',
            'OUTPUT': '/Users/malenahedemann/Desktop/Clases herramientas/Clase 4/languages_by_country.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
###################################################################
        # Intersection
###################################################################
        alg_params = {
            'INPUT': outputs['FixGeometriesWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['FixGeometriesCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        Intersection = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']
        return results

    def name(self):
        return 'model4a'

    def displayName(self):
        return 'model4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4a()
