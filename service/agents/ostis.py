from enum import Enum
import sc_client.client as client
from sc_client.models import (
    ScAddr,
    ScEventParams,
    ScConstruction,
    ScIdtfResolveParams,
    ScLinkContent,
    ScLinkContentType,
    ScTemplate,
)
from sc_client.constants.common import ScEventType
from sc_client.constants import sc_types
from threading import Event  # Import Event for signaling

from service.agents.abstract.auth_agent import AuthAgent, RegStatus, AuthStatus
from service.agents.abstract.navigation_agent import NavigationAgent
from service.agents.abstract.recommendation_agent import RecommendationAgent
from service.agents.abstract.blood_test_agent import BloodTestAgent
from config import Config
from service.exceptions import AgentError

# Initialize payload and event
payload = None
callback_event = Event()


def create_link(client, content: str):
    construction = ScConstruction()
    to_find_content = ScLinkContent(content, ScLinkContentType.STRING)
    construction.create_link(sc_types.LINK_CONST, to_find_content)
    link = client.create_elements(construction)
    return link[0]


def get_node(client) -> ScAddr:
    construction = ScConstruction()
    construction.create_node(sc_types.NODE_CONST)
    main_node: ScAddr = client.create_elements(construction)[0]
    return main_node


def call_back(src: ScAddr, connector: ScAddr, trg: ScAddr) -> Enum:
    global payload
    callback_event.clear()  # Clear the event at the start of callback

    succ_node = client.resolve_keynodes(
        ScIdtfResolveParams(idtf='action_finished_successfully', type=sc_types.NODE_CONST_CLASS)
    )[0]
    unsucc_node = client.resolve_keynodes(
        ScIdtfResolveParams(idtf='action_finished_unsuccessfully', type=sc_types.NODE_CONST_CLASS)
    )[0]
    node_err = client.resolve_keynodes(
        ScIdtfResolveParams(idtf='action_finished_with_error', type=sc_types.NODE_CONST_CLASS)
    )[0]

    if trg.value == succ_node.value:
        nrel_result = client.resolve_keynodes(
            ScIdtfResolveParams(idtf='nrel_result', type=sc_types.NODE_CONST_CLASS)
        )[0]
        res_templ = ScTemplate()
        res_templ.triple_with_relation(
            src,
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.NODE_VAR_STRUCT >> "_res_struct",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            nrel_result
        )
        res_templ.triple(
            "_res_struct",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.LINK_VAR >> "_link_res"
        )
        gen_res = client.template_search(res_templ)[0]
        link_res = gen_res.get("_link_res")
        link_data = client.get_link_content(link_res)[0].data
        payload = link_data
    elif trg.value == unsucc_node.value or trg.value == node_err.value:
        raise AgentError

    callback_event.set()
    if not payload:
        return result.FAILURE
    return result.SUCCESS


def call_back_multiple(src: ScAddr, connector: ScAddr, trg: ScAddr) -> Enum:
    global payload
    callback_event.clear()  # Clear the event at the start of callback

    succ_node = client.resolve_keynodes(
        ScIdtfResolveParams(idtf='action_finished_successfully', type=sc_types.NODE_CONST_CLASS)
    )[0]
    unsucc_node = client.resolve_keynodes(
        ScIdtfResolveParams(idtf='action_finished_unsuccessfully', type=sc_types.NODE_CONST_CLASS)
    )[0]
    node_err = client.resolve_keynodes(
        ScIdtfResolveParams(idtf='action_finished_with_error', type=sc_types.NODE_CONST_CLASS)
    )[0]

    if trg.value == succ_node.value:
        nrel_result = client.resolve_keynodes(
            ScIdtfResolveParams(idtf='nrel_result', type=sc_types.NODE_CONST_CLASS)
        )[0]
        res_templ = ScTemplate()
        res_templ.triple_with_relation(
            src,
            sc_types.EDGE_D_COMMON_VAR,
            sc_types.NODE_VAR_STRUCT >> "_res_struct",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            nrel_result
        )
        res_templ.triple(
            "_res_struct",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.LINK_VAR >> "_node_res"
        )
        diseases_result = []
        for gen_res in client.template_search(res_templ):
            link_res = gen_res.get("_node_res")
            link_data = client.get_link_content(link_res)[0].data
            diseases_result.append(link_data)

        payload = diseases_result
    elif trg.value == unsucc_node.value or trg.value == node_err.value:
        raise AgentError

    callback_event.set()
    if not payload:
        return result.FAILURE
    return result.SUCCESS


class result(Enum):
    SUCCESS = 0
    FAILURE = 1


class Ostis:
    def __init__(self, url):
        self.ostis_url = url

    def call_agent(self, action_name: str, username, password) -> str:
        client.connect(self.ostis_url)
        username_lnk = create_link(client, username)
        password_lnk = create_link(client, password)
        rrel_1 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_1', type=sc_types.NODE_CONST_ROLE))[0]
        rrel_2 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_2', type=sc_types.NODE_CONST_ROLE))[0]
        initiated_node = client.resolve_keynodes(ScIdtfResolveParams(idtf='action_initiated', type=sc_types.NODE_CONST_CLASS))[0]
        action_agent = client.resolve_keynodes(ScIdtfResolveParams(idtf=action_name, type=sc_types.NODE_CONST_CLASS))[0]
        main_node = get_node(client)

        template = ScTemplate()
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            username_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_1
        )
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            password_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_2
        )
        template.triple(
            action_agent,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )
        template.triple(
            initiated_node,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )

        event_params = ScEventParams(main_node, ScEventType.ADD_INGOING_EDGE, call_back)
        client.events_create(event_params)
        client.template_generate(template)

        global payload
        if callback_event.wait(timeout=10):
            while not payload:
                continue
            return payload
        else:
            raise AgentError(524, "Timeout")

    def call_agent_blood_test(self, wbc_val: float, rbc_val: float, platelets_val: float, node_lang="rus") -> None:
        client.connect(self.ostis_url)
        wbc_lnk = create_link(client, str(wbc_val))
        rbc_lnk = create_link(client, str(rbc_val))
        platelets_lnk = create_link(client, str(platelets_val))
        node_lang_lnk = create_link(client, node_lang)

        rrel_1 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_1', type=sc_types.NODE_CONST_ROLE))[0]
        rrel_2 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_2', type=sc_types.NODE_CONST_ROLE))[0]
        rrel_3 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_3', type=sc_types.NODE_CONST_ROLE))[0]
        rrel_4 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_4', type=sc_types.NODE_CONST_ROLE))[0]

        initiated_node = client.resolve_keynodes(ScIdtfResolveParams(idtf='action_initiated', type=sc_types.NODE_CONST_CLASS))[0]
        action_agent = client.resolve_keynodes(ScIdtfResolveParams(idtf="action_blood_test", type=sc_types.NODE_CONST_CLASS))[0]
        main_node = get_node(client)

        template = ScTemplate()
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            wbc_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_1
        )
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rbc_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_2
        )
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            platelets_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_3
        )
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            node_lang_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_4
        )
        template.triple(
            action_agent,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )
        template.triple(
            initiated_node,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )

        event_params = ScEventParams(main_node, ScEventType.ADD_INGOING_EDGE, call_back_multiple)
        client.events_create(event_params)
        client.template_generate(template)

        # Wait for the callback with a timeout
        global payload
        if callback_event.wait(timeout=10):
            while not payload:
                continue
            return payload  # Return the payload if event is set
        else:
            raise AgentError(524, "Timeout")

    def call_navigation_agent(self, node_name: str, node_lang="rus") -> None:
        global payload
        client.connect(self.ostis_url)
        node_lnk = create_link(client, node_name)
        node_lang_lnk = create_link(client, node_lang)

        rrel_1 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_1', type=sc_types.NODE_CONST_ROLE))[0]
        rrel_2 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_2', type=sc_types.NODE_CONST_ROLE))[0]

        initiated_node = client.resolve_keynodes(ScIdtfResolveParams(idtf='action_initiated', type=sc_types.NODE_CONST_CLASS))[0]
        action_agent = client.resolve_keynodes(ScIdtfResolveParams(idtf="action_navigate", type=sc_types.NODE_CONST_CLASS))[0]
        main_node = get_node(client)

        template = ScTemplate()
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            node_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_1
        )
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            node_lang_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_2
        )
        template.triple(
            action_agent,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )
        template.triple(
            initiated_node,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )

        event_params = ScEventParams(main_node, ScEventType.ADD_INGOING_EDGE, call_back)
        client.events_create(event_params)
        client.template_generate(template)

        global payload
        if callback_event.wait(timeout=10):
            while not payload:
                continue
            return payload
        else:
            raise AgentError(524, "Timeout")

    def call_recomendation_agent(self, node_name: str) -> None:
        global payload
        client.connect(self.ostis_url)
        node_lnk = create_link(client, node_name)

        rrel_1 = client.resolve_keynodes(ScIdtfResolveParams(idtf='rrel_1', type=sc_types.NODE_CONST_ROLE))[0]

        initiated_node = client.resolve_keynodes(ScIdtfResolveParams(idtf='action_initiated', type=sc_types.NODE_CONST_CLASS))[0]
        action_agent = client.resolve_keynodes(ScIdtfResolveParams(idtf="action_rec", type=sc_types.NODE_CONST_CLASS))[0]
        main_node = get_node(client)

        template = ScTemplate()
        template.triple_with_relation(
            main_node >> "_main_node",
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            node_lnk,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            rrel_1
        )
        template.triple(
            action_agent,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )
        template.triple(
            initiated_node,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            "_main_node",
        )

        event_params = ScEventParams(main_node, ScEventType.ADD_INGOING_EDGE, call_back)
        client.events_create(event_params)
        client.template_generate(template)

        global payload
        if callback_event.wait(timeout=10):
            while not payload:
                continue
            return payload
        else:
            raise AgentError(524, "Timeout")


class OstisAuthAgent(AuthAgent):
    def __init__(self):
        self.ostis = Ostis(Config.OSTIS_URL)

    def reg_agent(self, username: str, password: str):
        global payload
        payload = None
        agent_response = self.ostis.call_agent("action_reg", username, password)
        if agent_response == "User created":
            return {"status": RegStatus.CREATED}
        elif agent_response == "User exists":
            return {
                "status": RegStatus.EXISTS,
                "message": "User with that credentials already exists.",
                }
        raise AgentError

    def auth_agent(self, username: str, password: str):
        global payload
        payload = None
        agent_response = self.ostis.call_agent("action_auth", username, password)
        if agent_response == "Valid":
            return {"status": AuthStatus.VALID}
        elif agent_response == "Invalid":
            return {
                "status": AuthStatus.INVALID,
                "message": "Invalid credentials",
            }
        raise AgentError


class OstisBloodTestAgent(BloodTestAgent):
    def __init__(self):
        self.ostis = Ostis(Config.OSTIS_URL)

    def execute(self, wbc_val: float, rbc_val: float, platelets_val: float, node_lang: str = "rus"):
        global payload
        payload = None
        return {"message": self.ostis.call_agent_blood_test(wbc_val, rbc_val, platelets_val, node_lang)}


class OstisRecommendationAgent(RecommendationAgent):
    def __init__(self):
        self.ostis = Ostis(Config.OSTIS_URL)

    def execute(self, node_name: str):
        global payload
        payload = None
        return {"message": self.ostis.call_recomendation_agent(node_name)}


class OstisNavigationAgent(NavigationAgent):
    def __init__(self):
        self.ostis = Ostis(Config.OSTIS_URL)

    def execute(self, node_name: str, node_lang: str = "rus"):
        global payload
        payload = None
        return {"message": self.ostis.call_navigation_agent(node_name, node_lang)}
