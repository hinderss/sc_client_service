from .abstract.auth_agent import AuthAgent, RegStatus, AuthStatus
from .abstract.blood_hormones_test_agent import BloodHormonesTestAgent
from .abstract.blood_test_agent import BloodTestAgent
from .abstract.blood_micronutrients import BloodMicronutrientsAgent
from .abstract.blood_analysis import BloodVitaminAgent
from .abstract.navigation_agent import NavigationAgent
from .abstract.recommendation_agent import RecommendationAgent
from ..exceptions import AgentError


class OstisAuthAgent(AuthAgent):
    def reg_agent(self, username: str, password: str):
        print(f"MockAgent: Pretend registering {username} - {password}")
        return {"status": RegStatus.EXISTS}

    def auth_agent(self, username: str, password: str):
        print(f"MockAgent: Pretend authenticating {username} - {password}")
        # raise AgentError
        return {
            "status": AuthStatus.VALID,
            "message": "Invalid credentials",
        }


class OstisBloodTestAgent(BloodTestAgent):
    def execute(self, wbc_val: float, rbc_val: float, platelets_val: float, node_lang: str = "rus"):
        print(f"MockAgent: Pretend blood_test wbc={wbc_val}, rbc={rbc_val}, platelets={platelets_val} - language={node_lang}")
        # return {'message': None}
        return {'message': ['blood_test_for_cholangitis', 'blood_test_for_dacryoadenitis', 'blood_test_for_appendicitis', 'blood_test_for_brain_abscess', 'blood_test_for_meningitis', 'blood_test_for_stomach_cancer', 'blood_test_for_cholecystitis', 'blood_test_for_stroke', 'blood_test_for_encephalitis', 'blood_test_for_sinusitis']}


class OstisRecommendationAgent(RecommendationAgent):
    def execute(self, node_name: str):
        print(f"MockAgent: Pretend recommendation query={node_name}")
        return {'message': 'Важно контролировать уровень сахара в крови через диету, физические упражнения и, при необходимости, инсулин или другие медикаменты. Регулярные осмотры помогают предотвратить осложнения. Соблюдайте диету с низким содержанием сахара и углеводов.'}


class OstisNavigationAgent(NavigationAgent):
    def execute(self, node_name: str, node_lang: str = "rus"):
        print(f"MockAgent: Pretend navigation query={node_name}, language={node_lang}")
        return {'message': "Диабет - это хроническое заболевание, которое возникает либо в случаях, когда поджелудочная железа не вырабатывает достаточное количество инсулина, либо когда организм не может эффективно использовать вырабатываемый инсулин.\n∍немаксимальный класс объектов исследования':\n* Предметная область болезней\n* Предметная область болезней ЖКТ\n<=>эквиваленция*:\nнедостаточное производство инсулина\n<=причины возникновения:\nэнцефалопатия\n=>причины возникновения:\n* генетическая предрасположенность\n* сердечно-сосудистые заболевания\n* ухудшение иммунитета\n=>осложнения заболеваний:\n* диабетическая стопа\n* стенокардия\n* нефропатия\n* полиневропатия\n* ретинопатия\n* инфаркт миокарда\n=>классификация:\n* сахарный диабет 2 типа\n* гестационный диабет\n* сахарный диабет 1 типа\n=>симптом:\n* жажда\n* увеличенное мочеиспускание\n* размытое зрение\n* потеря веса\n* увеличенная усталость\n* боль при диабете\n=> метаболическое расстройство\n∊ blood_test_for_diabetes\n∊ болезнь\n∊ заболевание желудочно-кишечного тракта\n"}


class OstisBloodMicronutrientsAgent(BloodMicronutrientsAgent):
    def execute(self, ca_val: float, mg_val: float, fe_val: float):
        print(f"MockAgent: Pretend blood_micronutrients_test ca={ca_val}, mg={mg_val}, fe={fe_val}")
        # return {'message': None}
        return {'message': ["Кальций", "Магний", "Железо"]}


class OstisBloodVitaminAgent(BloodVitaminAgent):
    def execute(
            self,
            vitamin_e: float,
            vitamin_d: float,
            vitamin_k: float,
            vitamin_c: float,
            vitamin_b1: float,
            vitamin_b2: float,
            vitamin_b9: float,
            vitamin_b12: float,
            vitamin_a: float,
            vitamin_b6: float,
    ):
        print(
            f"MockAgent: Pretend blood_vitamin_test "
            f"vitamin_e={vitamin_e}, vitamin_d={vitamin_d}, vitamin_k={vitamin_k}, "
            f"vitamin_c={vitamin_c}, vitamin_b1={vitamin_b1}, vitamin_b2={vitamin_b2}, "
            f"vitamin_b9={vitamin_b9}, vitamin_b12={vitamin_b12}, vitamin_a={vitamin_a}, vitamin_b6={vitamin_b6}"
        )
        # return {'message': None}
        return {'message': ['blood_test_for_cholangitis', 'blood_test_for_dacryoadenitis', 'blood_test_for_appendicitis', 'blood_test_for_brain_abscess', 'blood_test_for_meningitis', 'blood_test_for_stomach_cancer', 'blood_test_for_cholecystitis', 'blood_test_for_stroke', 'blood_test_for_encephalitis', 'blood_test_for_sinusitis']}


class OstisHormonesBloodTestAgent(BloodHormonesTestAgent):
    def execute(self, tsh_val: float, fsh_val: float, lh_val: float, node_lang: str = "rus"):
        print(f"MockAgent: Pretend blood_hormones_test tsh={tsh_val}, fsh={fsh_val}, lh={lh_val} - language={node_lang}")
        # return {'message': None}
        return {'message': ['blood_test_for_cholangitis', 'blood_test_for_dacryoadenitis', 'blood_test_for_appendicitis', 'blood_test_for_brain_abscess', 'blood_test_for_meningitis', 'blood_test_for_stomach_cancer', 'blood_test_for_cholecystitis', 'blood_test_for_stroke', 'blood_test_for_encephalitis', 'blood_test_for_sinusitis']}

