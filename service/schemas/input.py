from marshmallow import Schema, fields, pre_load


class AuthSchema(Schema):
    username = fields.Str(
        required=True,
        error_messages={"required": "Username is required."},
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "Password is required."},
    )


class QuerySchema(Schema):
    query = fields.Str(required=True, error_messages={"required": "Search query is required."})
    language = fields.Str(required=False, default="rus", allow_none=True)

    @pre_load
    def process_inputs(self, data, **kwargs):
        if 'query' in data and isinstance(data['query'], str):
            data['query'] = data['query'].lower()
        if 'language' in data and isinstance(data['language'], str):
            data['language'] = data['language'].lower()
        return data


class BloodSchema(Schema):
    wbc = fields.Float(required=True)
    rbc = fields.Float(required=True)
    platelets = fields.Float(required=True)


class BloodAnalysisSchema(Schema):
    vitamin_e = fields.Float(required=True)
    vitamin_d = fields.Float(required=True)
    vitamin_k = fields.Float(required=True)
    vitamin_c = fields.Float(required=True)
    vitamin_b1 = fields.Float(required=True)
    vitamin_b2 = fields.Float(required=True)
    vitamin_b9 = fields.Float(required=True)
    vitamin_b12 = fields.Float(required=True)
    vitamin_a = fields.Float(required=True)
    vitamin_b6 = fields.Float(required=True)


class BloodMicronutrientsSchema(Schema):
    ca = fields.Float(required=True)
    mg = fields.Float(required=True)
    fe = fields.Float(required=True)


class BloodHormonesSchema(Schema):
    tsh = fields.Float(required=True)
    fsh = fields.Float(required=True)
    lh = fields.Float(required=True)


class DiagnosisSchema(Schema):
    symptoms = fields.List(fields.Str, required=True)
