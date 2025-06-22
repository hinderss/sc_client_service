from .abstract.auth_agent import AuthAgent, RegStatus, AuthStatus
from .abstract.blood_hormones_test_agent import BloodHormonesTestAgent
from .abstract.blood_test_agent import BloodTestAgent
from .abstract.blood_micronutrients import BloodMicronutrientsAgent
from .abstract.blood_analysis import BloodVitaminAgent
from .abstract.diagnosis_agent import DiagnosisAgent
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
        # Нормальные диапазоны показателей крови (можете уточнить у врачей)
        NORMAL_WBC = (4.0, 10.0)  # 10^9/л
        NORMAL_RBC = (3.8, 5.8)  # 10^12/л (женщины: 3.8-5.1, мужчины: 4.3-5.8)
        NORMAL_PLATELETS = (150, 450)  # 10^9/л

        possible_diseases = []

        # Анализ WBC (лейкоциты)
        if wbc_val > NORMAL_WBC[1]:  # Лейкоцитоз
            possible_diseases.extend([
                "blood_test_for_appendicitis",
                "blood_test_for_cholangitis",
                "blood_test_for_cholecystitis",
                "blood_test_for_meningitis",
                "blood_test_for_encephalitis",
                "blood_test_for_pneumonia",
                "blood_test_for_acute_tonsillitis",
                "blood_test_for_bronchitis",
                "blood_test_for_sinusitis",
                "blood_test_for_laryngitis",
                "blood_test_for_pharyngitis",
                "blood_test_for_flu",
                "blood_test_for_brain_abscess"
            ])
        elif wbc_val < NORMAL_WBC[0]:  # Лейкопения
            possible_diseases.extend([
                "blood_test_for_hepatitis",
                "blood_test_for_cirrhosis_of_the_liver",
                "blood_test_for_encephalopathy",
                "blood_test_for_lung_cancer",
                "blood_test_for_stomach_cancer"
            ])

        # Анализ RBC (эритроциты)
        if rbc_val > NORMAL_RBC[1]:  # Эритроцитоз
            possible_diseases.extend([
                "blood_test_for_chronic_pancreatitis",
                "blood_test_for_cirrhosis_of_the_liver",
                "blood_test_for_intestinal_atony",
                "blood_test_for_intracranial_hypertension"
            ])
        elif rbc_val < NORMAL_RBC[0]:  # Анемия
            possible_diseases.extend([
                "blood_test_for_celiac_disease",
                "blood_test_for_chronic_diarrhea",
                "blood_test_for_crohns_disease",
                "blood_test_for_peptic_ulcer_of_stomach",
                "blood_test_for_gastriris",
                "blood_test_for_duodenitis",
                "blood_test_for_esophagitis",
                "blood_test_for_stomach_cancer",
                "blood_test_for_lung_cancer",
                "blood_test_for_chronic_obstructive_pulmonary_disease"
            ])

        # Анализ тромбоцитов
        if platelets_val > NORMAL_PLATELETS[1]:  # Тромбоцитоз
            possible_diseases.extend([
                "blood_test_for_cirrhosis_of_the_liver",
                "blood_test_for_chronic_pancreatitis",
                "blood_test_for_intestinal_atony",
                "blood_test_for_rheumatoid_arthritis"
            ])
        elif platelets_val < NORMAL_PLATELETS[0]:  # Тромбоцитопения
            possible_diseases.extend([
                "blood_test_for_hepatitis",
                "blood_test_for_cirrhosis_of_the_liver",
                "blood_test_for_encephalopathy",
                "blood_test_for_meningitis",
                "blood_test_for_dysbacteriosis"
            ])

        # Специфические комбинации показателей
        if wbc_val > NORMAL_WBC[1] and platelets_val < NORMAL_PLATELETS[0]:
            possible_diseases.append("blood_test_for_meningitis")

        if wbc_val > NORMAL_WBC[1] and rbc_val < NORMAL_RBC[0]:
            possible_diseases.append("blood_test_for_pneumonia")

        if platelets_val > NORMAL_PLATELETS[1] and rbc_val < NORMAL_RBC[0]:
            possible_diseases.append("blood_test_for_stomach_cancer")

        # Удаляем дубликаты
        possible_diseases = list(set(possible_diseases))

        return {'message': possible_diseases}


blood_test_data = {
    "blood_test_for_appendicitis": {
        "result": "Аппендицит",
        "recommendation": "Экстренная хирургическая консультация. Аппендэктомия. До осмотра: голод, холод на живот, запрет анальгетиков."
    },
    "blood_test_for_celiac_disease": {
        "result": "Целиакия",
        "recommendation": "Строгая безглютеновая диета. Контроль антител к тканевой трансглутаминазе. Витаминотерапия."
    },
    "blood_test_for_cholangitis": {
        "result": "Холангит",
        "recommendation": "Срочная госпитализация. Антибиотикотерапия (цефтриаксон+метронидазол). ЭРХПГ для дренирования."
    },
    "blood_test_for_cholecystitis": {
        "result": "Холецистит",
        "recommendation": "Голод, спазмолитики, антибиотики. Плановая холецистэктомия при калькулезной форме."
    },
    "blood_test_for_cholelithiasis": {
        "result": "Желчнокаменная болезнь",
        "recommendation": "УЗИ контроль. При колике - спазмолитики. Показания к холецистэктомии."
    },
    "blood_test_for_chronic_diarrhea": {
        "result": "Хроническая диарея",
        "recommendation": "Копрограмма, колоноскопия. Коррекция водно-электролитного баланса. Этиотропное лечение."
    },
    "blood_test_for_chronic_pancreatitis": {
        "result": "Хронический панкреатит",
        "recommendation": "Диета №5п. Панкреатин. Исключение алкоголя. Контроль глюкозы."
    },
    "blood_test_for_cirrhosis_of_the_liver": {
        "result": "Цирроз печени",
        "recommendation": "Гепатопротекторы. Диета с ограничением белка. Мониторинг осложнений."
    },
    "blood_test_for_crohns_disease": {
        "result": "Болезнь Крона",
        "recommendation": "Месалазин, глюкокортикоиды. Регулярная колоноскопия. Диета."
    },
    "blood_test_for_diabetes": {
        "result": "Сахарный диабет",
        "recommendation": "Диета №9. Контроль гликемии. Инсулин или пероральные сахароснижающие препараты."
    },
    "blood_test_for_diverticulosis": {
        "result": "Дивертикулёз",
        "recommendation": "Диета с высоким содержанием клетчатки. При воспалении - антибиотики."
    },
    "blood_test_for_duodenitis": {
        "result": "Дуоденит",
        "recommendation": "Диета №1. Ингибиторы протонной помпы. Эрадикация H.pylori при обнаружении."
    },
    "blood_test_for_dysbacteriosis": {
        "result": "Дисбактериоз",
        "recommendation": "Пробиотики. Коррекция диеты. Лечение основного заболевания."
    },
    "blood_test_for_esophagitis": {
        "result": "Эзофагит",
        "recommendation": "Ингибиторы протонной помпы. Щадящая диета. Эндоскопический контроль."
    },
    "blood_test_for_gastriris": {
        "result": "Гастрит",
        "recommendation": "Диета №1. Эрадикация H.pylori. Антациды при необходимости."
    },
    "blood_test_for_gastroesophageal_reflux_disease": {
        "result": "ГЭРБ",
        "recommendation": "Ингибиторы протонной помпы. Диета. Сон с приподнятым головным концом."
    },
    "blood_test_for_hepatitis": {
        "result": "Гепатит",
        "recommendation": "Определение этиологии. Гепатопротекторы. При вирусных - специфическая терапия."
    },
    "blood_test_for_intestinal_atony": {
        "result": "Атония кишечника",
        "recommendation": "Прокинетики. Диета с клетчаткой. ЛФК. Лечение основного заболевания."
    },
    "blood_test_for_lactose_intolerance": {
        "result": "Непереносимость лактозы",
        "recommendation": "Безлактозная диета. Фермент лактаза при необходимости."
    },
    "blood_test_for_peptic_ulcer_of_stomach": {
        "result": "Язва желудка",
        "recommendation": "Эрадикация H.pylori. Ингибиторы протонной помпы. Диета №1."
    },
    "blood_test_for_pneumatosis": {
        "result": "Пневматоз",
        "recommendation": "Лечение основного заболевания. Диета. При осложнениях - хирургическое лечение."
    },
    "blood_test_for_irritable_bowel_syndrome": {
        "result": "СРК",
        "recommendation": "Коррекция диеты. Спазмолитики. Психотерапия при необходимости."
    },
    "blood_test_for_stomach_cancer": {
        "result": "Рак желудка",
        "recommendation": "ЭГДС с биопсией. КТ. Консультация онколога. Хирургическое лечение."
    },
    "blood_test_for_brain_tumor": {
        "result": "Опухоль мозга",
        "recommendation": "МРТ с контрастом. Консультация нейрохирурга. Биопсия. Тактика зависит от типа опухоли."
    },
    "blood_test_for_encephalitis": {
        "result": "Энцефалит",
        "recommendation": "Экстренная госпитализация. Этиотропная терапия. Мониторинг неврологического статуса."
    },
    "blood_test_for_epilepsy": {
        "result": "Эпилепсия",
        "recommendation": "ЭЭГ. МРТ. Противоэпилептические препараты. Регулярный неврологический контроль."
    },
    "blood_test_for_meningitis": {
        "result": "Менингит",
        "recommendation": "Люмбальная пункция. Антибиотики. Дексаметазон. Интенсивная терапия."
    },
    "blood_test_for_parkinsons_disease": {
        "result": "Болезнь Паркинсона",
        "recommendation": "Леводопа. Агонисты дофаминовых рецепторов. ЛФК. Нейропротективная терапия."
    },
    "blood_test_for_stroke": {
        "result": "Инсульт",
        "recommendation": "Экстренная госпитализация. КТ. В первые 4,5 часа - тромболизис. Реабилитация."
    },
    "blood_test_for_brain_abscess": {
        "result": "Абсцесс мозга",
        "recommendation": "Антибиотики. Хирургическое дренирование. Контроль МРТ."
    },
    "blood_test_for_encephalopathy": {
        "result": "Энцефалопатия",
        "recommendation": "Лечение основного заболевания. Нейропротекторы. Симптоматическая терапия."
    },
    "blood_test_for_intracranial_hypertension": {
        "result": "ВЧГ",
        "recommendation": "Мочегонные. Контроль ликворного давления. Лечение причины."
    },
    "blood_test_for_meningioma": {
        "result": "Менингиома",
        "recommendation": "Наблюдение или хирургическое лечение в зависимости от размера и локализации."
    },
    "blood_test_for_vegeto_vascular_dystonia_of_brain_vessels": {
        "result": "ВСД",
        "recommendation": "Коррекция образа жизни. Седативные. Вегетотропные препараты. ЛФК."
    },
    "blood_test_for_aneurysm": {
        "result": "Аневризма",
        "recommendation": "Ангиография. Консультация сосудистого хирурга. При риске разрыва - оперативное лечение."
    },
    "blood_test_for_dacryoadenitis": {
        "result": "Дакриоаденит",
        "recommendation": "Антибиотикотерапия. Физиотерапия. При абсцедировании - дренирование."
    },
    "blood_test_for_nivrit": {
        "result": "Неврит",
        "recommendation": "Противовоспалительная терапия. Витамины группы B. Физиотерапия."
    },
    "blood_test_for_sinusitis": {
        "result": "Синусит",
        "recommendation": "Антибиотики. Сосудосуживающие. Пункция пазух при необходимости."
    },
    "blood_test_for_acute_tonsillitis": {
        "result": "Ангина",
        "recommendation": "Антибиотики пенициллинового ряда. Местные антисептики. Постельный режим."
    },
    "blood_test_for_allergic_rhinitis": {
        "result": "Аллергический ринит",
        "recommendation": "Антигистаминные. Назальные кортикостероиды. Аллерген-специфическая иммунотерапия."
    },
    "blood_test_for_bronchial_asthma": {
        "result": "Бронхиальная астма",
        "recommendation": "ИГКС+ДДБА. Купирование бронхоспазма. Аллергологическое обследование."
    },
    "blood_test_for_bronchitis": {
        "result": "Бронхит",
        "recommendation": "Противовирусные или антибиотики. Муколитики. Ингаляции."
    },
    "blood_test_for_chronic_obstructive_pulmonary_disease": {
        "result": "ХОБЛ",
        "recommendation": "Бронходилататоры. ИГКС. Кислородотерапия при необходимости."
    },
    "blood_test_for_flu": {
        "result": "Грипп",
        "recommendation": "Противовирусные (осельтамивир). Симптоматическое лечение. Постельный режим."
    },
    "blood_test_for_laryngitis": {
        "result": "Ларингит",
        "recommendation": "Голосовой покой. Ингаляции. Антигистаминные при отеке."
    },
    "blood_test_for_lung_cancer": {
        "result": "Рак легкого",
        "recommendation": "КТ с контрастом. Биопсия. Определение стадии. Химиолучевая терапия."
    },
    "blood_test_for_pharyngitis": {
        "result": "Фарингит",
        "recommendation": "Местные антисептики. Противовоспалительные. Щадящая диета."
    },
    "blood_test_for_pneumonia": {
        "result": "Пневмония",
        "recommendation": "Антибиотики. Рентген-контроль. Дыхательная гимнастика."
    },
    "blood_test_for_neuralgic_amyotrophy": {
        "result": "Невралгическая амиотрофия",
        "recommendation": "Кортикостероиды. Витамины группы B. Физиотерапия."
    },
    "blood_test_for_duchenne_muscular_dystrophy": {
        "result": "Мышечная дистрофия Дюшенна",
        "recommendation": "Глюкокортикоиды. ЛФК. Респираторная поддержка. Генетическое консультирование."
    },
    "blood_test_for_lambert_eaton_syndrome": {
        "result": "Синдром Ламберта-Итона",
        "recommendation": "Иммуносупрессанты. Ацетилхолинэстеразные ингибиторы. Лечение опухоли при паранеопластической форме."
    },
    "blood_test_for_miozit": {
        "result": "Миозит",
        "recommendation": "НПВС. Физиотерапия. При инфекционной этиологии - антибиотики."
    },
    "blood_test_for_myasthenia_gravis": {
        "result": "Миастения Гравис",
        "recommendation": "Антихолинэстеразные препараты. Иммуносупрессивная терапия. Тимэктомия при наличии тимомы."
    },
    "blood_test_for_rheumatoid_arthritis": {
        "result": "Ревматоидный артрит",
        "recommendation": "Метотрексат. НПВС. ГИБП. ЛФК. Регулярный контроль суставного статуса."
    },
    "blood_test_for_rhabdomyolysis": {
        "result": "Рабдомиолиз",
        "recommendation": "Инфузионная терапия. Коррекция электролитов. Гемодиализ при ОПН."
    },
    "blood_test_for_polymyalgia_rheumatica": {
        "result": "Ревматическая полимиалгия",
        "recommendation": "Глюкокортикоиды. Постепенная отмена. Контроль воспалительных маркеров."
    },
}


class OstisRecommendationAgent(RecommendationAgent):
    def execute(self, diagnosis: str):
        for test_key, test_data in blood_test_data.items():
            if test_data['result'].lower() == diagnosis.lower():
                return {
                    # 'result': diagnosis,
                    'message': test_data['recommendation']
                }

        return {
            'message': f'Рекомендации для диагноза "{diagnosis}" не найдены. Пожалуйста, проконсультируйтесь с врачом.'
        }


class OstisNavigationAgent(NavigationAgent):
    def execute(self, node_name: str, node_lang: str = "rus"):
        print(f"MockAgent: Pretend navigation query={node_name}, language={node_lang}")
        return {'message': "Диабет - это хроническое заболевание, которое возникает либо в случаях, когда поджелудочная железа не вырабатывает достаточное количество инсулина, либо когда организм не может эффективно использовать вырабатываемый инсулин.\n∍немаксимальный класс объектов исследования':\n* Предметная область болезней\n* Предметная область болезней ЖКТ\n<=>эквиваленция*:\nнедостаточное производство инсулина\n<=причины возникновения:\nэнцефалопатия\n=>причины возникновения:\n* генетическая предрасположенность\n* сердечно-сосудистые заболевания\n* ухудшение иммунитета\n=>осложнения заболеваний:\n* диабетическая стопа\n* стенокардия\n* нефропатия\n* полиневропатия\n* ретинопатия\n* инфаркт миокарда\n=>классификация:\n* сахарный диабет 2 типа\n* гестационный диабет\n* сахарный диабет 1 типа\n=>симптом:\n* жажда\n* увеличенное мочеиспускание\n* размытое зрение\n* потеря веса\n* увеличенная усталость\n* боль при диабете\n=> метаболическое расстройство\n∊ blood_test_for_diabetes\n∊ болезнь\n∊ заболевание желудочно-кишечного тракта\n"}


class OstisBloodMicronutrientsAgent(BloodMicronutrientsAgent):
    def execute(self, ca_val: float, mg_val: float, fe_val: float):
        CA_LOWER, CA_UPPER = 2.1, 2.6  # ммоль/л
        MG_LOWER, MG_UPPER = 0.7, 1.1  # ммоль/л
        FE_LOWER, FE_UPPER = 9.0, 30.0  # мкмоль/л

        results = []

        if ca_val < CA_LOWER:
            results.append({"calcium": "deficiency"})
        elif ca_val > CA_UPPER:
            results.append({"calcium": "excess"})

        if mg_val < MG_LOWER:
            results.append({"magnesium": "deficiency"})
        elif mg_val > MG_UPPER:
            results.append({"magnesium": "excess"})

        if fe_val < FE_LOWER:
            results.append({"iron": "deficiency"})
        elif fe_val > FE_UPPER:
            results.append({"iron": "excess"})

        return {'message': results}


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

        # Reference ranges (may vary by lab)
        vitamin_ranges = {
            "vitamin_e": (5.7, 19.9),    # mg/L
            "vitamin_d": (30, 100),      # ng/mL
            "vitamin_k": (0.2, 3.2),     # ng/mL
            "vitamin_c": (0.4, 2.0),     # mg/dL
            "vitamin_b1": (2.5, 7.5),    # µg/dL
            "vitamin_b2": (4, 24),       # µg/dL
            "vitamin_b9": (3.1, 20.5),   # ng/mL
            "vitamin_b12": (200, 900),   # pg/mL
            "vitamin_a": (0.3, 0.8),     # mg/L
            "vitamin_b6": (5, 30)        # ng/mL
        }

        results = []
        vitamins = {
            "vitamin_e": vitamin_e,
            "vitamin_d": vitamin_d,
            "vitamin_k": vitamin_k,
            "vitamin_c": vitamin_c,
            "vitamin_b1": vitamin_b1,
            "vitamin_b2": vitamin_b2,
            "vitamin_b9": vitamin_b9,
            "vitamin_b12": vitamin_b12,
            "vitamin_a": vitamin_a,
            "vitamin_b6": vitamin_b6
        }

        for vitamin, value in vitamins.items():
            lower, upper = vitamin_ranges[vitamin]
            if value < lower:
                results.append({vitamin: "deficiency"})
            elif value > upper:
                results.append({vitamin: "excess"})

        return {'message': results}


class OstisHormonesBloodTestAgent(BloodHormonesTestAgent):
    def execute(self, tsh_val: float, fsh_val: float, lh_val: float, node_lang: str = "rus") -> dict[str, list[str]]:
        """
        Анализ гормонов и возврат списка возможных заболеваний
        Возвращает только кодовые названия болезней
        """
        detected_diseases = []

        # Гипотиреоз (высокий ТТГ)
        if tsh_val > 4.0:
            detected_diseases.append("blood_test_for_hypothyroidism")
            detected_diseases.append("blood_test_for_hashimotos_thyroiditis")

        # Гипертиреоз (низкий ТТГ)
        elif tsh_val < 0.4:
            detected_diseases.append("blood_test_for_hyperthyroidism")

        # Гипопитуитаризм (низкие все гормоны)
        if tsh_val < 0.4 and fsh_val < 1.5 and lh_val < 1.5:
            detected_diseases.append("blood_test_for_hypopituitarism")

        # Синдром Клайнфельтера (очень высокие ФСГ и ЛГ)
        if fsh_val > 20.0 and lh_val > 12.0:
            detected_diseases.append("blood_test_for_klinefelter_syndrome")

        # Гипогонадизм (высокие гонадотропины)
        elif fsh_val > 12.5 or lh_val > 9.0:
            detected_diseases.append("blood_test_for_hypogonadism")
            detected_diseases.append("blood_test_for_hypogonadotropic_hypogonadism")

        # Удаляем дубликаты
        detected_diseases = list(set(detected_diseases))

        return {'message': detected_diseases}


class OstisDiagnosisAgent(DiagnosisAgent):
    def __init__(self):
        # База знаний: симптомы для каждой болезни с весами
        self.disease_symptoms = {
            # ЖКТ заболевания
            'blood_test_for_appendicitis': {
                'symptoms': {
                    'Боль внизу живота': 0.9,
                    'Тошнота': 0.7,
                    'Отсутствие аппетита': 0.6,
                    'Повышенная температура': 0.5
                },
                'base_prob': 0.05  # Базовая вероятность в популяции
            },
            'blood_test_for_gastriris': {
                'symptoms': {
                    'Боль в груди': 0.7,
                    'Тошнота': 0.6,
                    'Отсутствие аппетита': 0.5
                },
                'base_prob': 0.1
            },
            'blood_test_for_peptic_ulcer_of_stomach': {
                'symptoms': {
                    'Боль в груди': 0.8,
                    'Тошнота': 0.7,
                    'Отсутствие аппетита': 0.6
                },
                'base_prob': 0.03
            },

            # Респираторные заболевания
            'blood_test_for_flu': {
                'symptoms': {
                    'Повышенная температура': 0.9,
                    'Недомогание': 0.8,
                    'Боль в горле': 0.7,
                    'Кашель': 0.6,
                    'Сонливость': 0.5
                },
                'base_prob': 0.2
            },
            'blood_test_for_pneumonia': {
                'symptoms': {
                    'Повышенная температура': 0.8,
                    'Кашель': 0.8,
                    'Боль в груди': 0.6,
                    'Недомогание': 0.7
                },
                'base_prob': 0.05
            },

            # Неврологические заболевания
            'blood_test_for_meningitis': {
                'symptoms': {
                    'Повышенная температура': 0.9,
                    'Чувствительность к свету': 0.8,
                    'Недомогание': 0.7,
                    'Сонливость': 0.6,
                    'Тошнота': 0.5
                },
                'base_prob': 0.01
            },

            # Эндокринные заболевания
            'blood_test_for_diabetes': {
                'symptoms': {
                    'Жажда': 0.9,
                    'Сухость кожи': 0.7,
                    'Недомогание': 0.5
                },
                'base_prob': 0.08
            },

            # ЛОР заболевания
            'blood_test_for_acute_tonsillitis': {
                'symptoms': {
                    'Боль в горле': 0.9,
                    'Повышенная температура': 0.8,
                    'Отсутствие аппетита': 0.5
                },
                'base_prob': 0.1
            },

            # Другие
            'blood_test_for_encephalitis': {
                'symptoms': {
                    'Повышенная температура': 0.8,
                    'Сонливость': 0.7,
                    'Тошнота': 0.6,
                    'Чувствительность к свету': 0.5
                },
                'base_prob': 0.005
            }
        }

    def execute(self, symptoms):
        results = []

        for disease, data in self.disease_symptoms.items():
            match_score = 0
            total_weight = 0

            # Проверяем каждый симптом болезни
            for symptom, weight in data['symptoms'].items():
                if symptom in symptoms:
                    match_score += weight
                total_weight += weight

            if total_weight > 0:
                # Рассчитываем вероятность с учетом базовой вероятности
                probability = (match_score / total_weight) * data['base_prob'] * 100
                if probability > 1:  # Порог для вывода
                    results.append({"disease": disease, "probability": round(probability, 2)})

        # Сортируем по убыванию вероятности
        # results.sort(key=lambda x: x[1], reverse=True)

        return {"message": results}
