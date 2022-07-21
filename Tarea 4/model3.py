
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
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

class Model3(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_fields_3', 'drop_fields_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_3', 'fixgeo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(7, model_feedback)
        results = {}
        outputs = {}
###################################################################
        # Fix geometries
###################################################################
        alg_params = {
            'INPUT': '/Users/malenahedemann/Desktop/Clases herramientas/Clase 4/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_3']
        }
        Fixgeo_3 = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Zonal statistics
###################################################################
        alg_params = {
            'COLUMN_PREFIX': 'pop1900',
            'INPUT': 'Zonal_Statistics_ce98237b_fb22_4575_bc48_5384798f2ff3',
            'INPUT_RASTER': 'popd_1900AD_7f06d32e_6eee_4a3a_9f5d_b2f8c8e91df1',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop1900']
        }
        Pop1900 = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True) ['OUTPUT']

###################################################################
        # Zonal statistics
###################################################################
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': 'Remaining_fields_32a6a7f0_b37c_455c_b885_6d7434ac4573',
            'INPUT_RASTER': 'landquality_2bd16ede_9368_44a4_a19e_943d576b282f',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Landq']
        }
        Landq = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Zonal statistics
###################################################################
        alg_params = {
            'COLUMN_PREFIX': 'pop2000',
            'INPUT': 'Zonal_Statistics_8d3b5251_afea_48aa_9ef1_b3593897a678',
            'INPUT_RASTER': 'popd_2000AD_6e9462d9_cc78_4288_8ea0_c75bea7bb047',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop2000']
        }
        Pop2000 = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Drop field(s)
###################################################################
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT',
                       'SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF',
                       'GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME',
                       'NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL',
                       'FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK',
                       'NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9',
                       'MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR',
                       'ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH',
                       'ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH',
                       'WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR',
                       'ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN',
                       'ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR',
                       'ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA',
                       'ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN',
                       'ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT',
                       'ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN',
                       'ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN',
                       'LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL',
                       'MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN',
                       'NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE',
                       'NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL',
                       'NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR',
                       'NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC',
                       'FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW',
                       'FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR',
                       'FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT',
                       'FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID',
                       'FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD',
                       'FCLASS_UA'],
            'INPUT': 'Fixed_geometries_c57983ac_5a78_49e8_9ad0_71a3aa6e9d56',
            'OUTPUT': parameters['Drop_fields_3']
        }
        Drop_fields_3 = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True) ['OUTPUT']


###################################################################
        # Zonal statistics
###################################################################
        alg_params = {
            'COLUMN_PREFIX': 'pop1800',
            'INPUT': 'Zonal_Statistics_1a1be2e5_e0a3_47aa_abb6_743274ca7736',
            'INPUT_RASTER': 'popd_1800AD_a6b8bff6_1796_4149_a579_5ed4d601717e',
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Pop1800']
        }
        oPop1800 = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)['OUTPUT']

###################################################################
        # Save vector features to file
###################################################################
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': 'Zonal_Statistics_52246135_f7f4_4fee_b599_63e040921229',
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': '/Users/malenahedemann/Desktop/Clases herramientas/Clase 4/models/model3.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model3'

    def displayName(self):
        return 'model3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model3()