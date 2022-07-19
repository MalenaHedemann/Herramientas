
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

mainpath = "/Users/malenahedemann/Desktop/Clases herramientas/Clase 4"
langa = "{}/langa/langa.shp".format(mainpath)

    
###################################################################
    #we create the model

class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Wldsout', 'wldsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Lenght', 'lenght', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}
###################################################################
        # Fix geometries
###################################################################
    
alg_params = {
            'INPUT': 'langa',
            'OUTPUT': parameters['Fix_geo']
        }
        Fix_geo = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Field calculator
###################################################################
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'lnm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # String
            'FORMULA': '"NAME_PROP"',
            'INPUT': 'menor_a_11_d6e1ada5_f27a_4cc7_bbec_a315f3dde214',
            'OUTPUT': parameters['Field_calc']
        }
        Field_calc = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Add autoincremental field
###################################################################
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'MODULUS': None,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        Autoinc_id = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True ['OUTPUT']

###################################################################
        # Drop field(s)
###################################################################
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': 'Calculated_b0e3c5c9_1197_4176_919d_b85bf66ab5e7',
            'OUTPUT': parameters['Wldsout']
        }
          Wldsout = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True) ['OUTPUT']

###################################################################
        # Field calculator
###################################################################
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'lenght',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': 'Incremented_34a08cd7_2b1e_4652_bb93_7e03a2ffc89c',
            'OUTPUT': parameters['Lenght']
        }
        Lenght = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True) ['OUTPUT']

###################################################################
        # Feature filter
###################################################################
        alg_params = {
            'INPUT': 'Calculated_17379727_7a47_4b13_ae52_b398eb4fc4c8',
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        Output_menor_a_11= processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT_menor_a_11']
        return results

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
