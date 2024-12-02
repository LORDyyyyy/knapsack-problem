from flask import Blueprint, jsonify, request, Response
from core import Knapsack, Genetic, UnboundedGenetic
from marshmallow import (
    Schema,
    fields,
    ValidationError,
    INCLUDE,
    validates_schema,
)


api_bp = Blueprint("api", __name__)


def positive_non_zero(value):
    if value <= 0:
        raise ValidationError("Must be a positive non-zero integer.")


class SolveRequestSchema(Schema):
    type = fields.Int(validate=lambda x: x in [1, 2], required=True)
    n = fields.Int(validate=positive_non_zero, required=True)
    maximum_capacity = fields.Int(validate=positive_non_zero, required=True)
    weight = fields.List(
        fields.Int(validate=positive_non_zero),
        required=True,
    )
    value = fields.List(
        fields.Int(validate=positive_non_zero),
        required=True,
    )

    @validates_schema
    def validate_length(self, data, **kwargs):
        if len(data["weight"]) != data["n"]:
            raise ValidationError(
                f"Length of 'weight' list must be equal to 'n', which is {data['n']}.",
                field_name="weight",
            )
        if len(data["value"]) != data["n"]:
            raise ValidationError(
                f"Length of 'value' list must be equal to 'n', which is {data['n']}.",
                field_name="value",
            )

    class Meta:
        unknown = INCLUDE


@api_bp.route("/api/")
def index():
    return jsonify({"message": "Working"}), 200


@api_bp.route("/api/solve", methods=["POST"])
def solve():
    try:
        schema = SolveRequestSchema()
        data = request.get_json()
        result = schema.load(data)

        problem_type = int(result["type"])
        n, Knapsack.maximum_capacity = int(result["n"]), int(result["maximum_capacity"])
        weight, value = result["weight"], result["value"]

        genetic = Genetic() if problem_type == 1 else UnboundedGenetic()

        for i in range(n):
            Knapsack.add_item(weight=int(weight[i]), value=int(value[i]))

        def wrapper():
            for knapsack, _ in genetic.evolution(lim=500):
                yield str(knapsack) + "\n"

        return Response(wrapper(), content_type="text/plain")

        # return Response(genetic.evolution(lim=500), content_type="text/plain")

    except ValidationError as err:
        return jsonify(err.messages), 400
