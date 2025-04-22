from testlink import TestlinkAPIClient
import xml.etree.ElementTree as ET
from config import reader_config as cfg
import traceback

class TestLinkUploader:
    def __init__(self):
        self.tlc = TestlinkAPIClient(cfg.TESTLINK_SERVER_URL, cfg.TESTLINK_DEV_KEY)
        self._cache_suites = {}

    def _get_or_create_suite(self, suite_name: str, project_id: int) -> int:
        try:
            print(f"📌 Proyecto configurado: {project_id}")

            # Validación previa
            all_projects = self.tlc.getProjects()
            print("📋 Proyectos disponibles:")
            for project in all_projects:
                print(f" - {project['name']} (ID: {project['id']})")

            if not any(str(p['id']) == str(project_id) for p in all_projects):
                raise Exception(f"❌ El proyecto con ID {project_id} no existe o no tienes permisos.")

            if suite_name in self._cache_suites:
                return self._cache_suites[suite_name]

            all_suites = self.tlc.getFirstLevelTestSuitesForTestProject(project_id)
            print(f"Proyecto info: {all_suites}")

            for suite in all_suites:
                if suite['name'] == suite_name:
                    self._cache_suites[suite_name] = int(suite['id'])
                    return int(suite['id'])

            new_suite = self.tlc.createTestSuite(
                testprojectid=project_id,
                testsuitename=suite_name,
                details='Creado automáticamente desde Excel'
            )

            print(f"Creación de suite: {new_suite}")
            suite_id = int(new_suite[0]['id'])
            self._cache_suites[suite_name] = suite_id
            return suite_id

        except Exception as e:
            print(f"❌ Error al manejar suite '{suite_name}': {str(e)}")
            traceback.print_exc()
            raise

    def _upload_testcase(self, project_id: int, suite_id: int, case_name: str, summary: str, steps: list, preconditions: str):
        try:
            tl_steps = [
                {
                    'step_number': str(step['step_number']),
                    'actions': step['actions'],
                    'expected_results': step.get('expectedresults', '')
                }
                for step in steps
            ]

            response = self.tlc.createTestCase(
                testcasename=case_name,
                testsuiteid=suite_id,
                testprojectid=project_id,
                authorlogin=cfg.TESTLINK_USER,
                summary=summary,
                preconditions=preconditions,
                steps=tl_steps,
                importance="2",
                executiontype="1"
            )
            return response
        except Exception as e:
            print(f"❌ Error subiendo caso '{case_name}': {str(e)}")
            raise

    def _parse_steps(self, testcase) -> list:
        return [
            {
                'step_number': step.findtext('step_number', '1').strip(),
                'actions': step.findtext('actions', '').strip(),
                'expectedresults': step.findtext('expectedresults', '').strip()
            }
            for step in testcase.findall('steps/step')
        ]

    def upload_from_xml(self, xml_file_path: str, project_id: int):
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            for testsuite in root.findall('testsuite'):
                suite_name = testsuite.get('name')
                print(f"📂 Procesando suite: {suite_name}")
                suite_id = self._get_or_create_suite(suite_name, project_id)

                for testcase in testsuite.findall('testcase'):
                    case_name = testcase.get('name')
                    print(f"   ⬆️ Subiendo caso: {case_name}")

                    self._upload_testcase(
                        project_id=project_id,
                        suite_id=suite_id,
                        case_name=case_name,
                        steps=self._parse_steps(testcase),
                        summary=testcase.findtext('summary', ''),
                        preconditions=testcase.findtext('preconditions', '')
                    )
            print("✅ Casos subidos exitosamente a TestLink")
        except Exception as e:
            print(f"❌ Error procesando XML: {str(e)}")
            raise

    def test_connection(self):
        try:
            projects = self.tlc.getProjects()
            print(f"Conexión exitosa. Proyectos disponibles: {projects}")
        except Exception as e:
            print(f"Error al conectar a TestLink: {str(e)}")
