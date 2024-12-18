from flask import Blueprint, jsonify, request, Response
from core import Knapsack, Genetic, UnboundedGenetic
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
from marshmallow import (
    Schema,
    fields,
    ValidationError,
    INCLUDE,
    validates_schema,
)
import io
import base64

mpl.use("Agg")


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

        # Clear Knapsack's available items
        Knapsack.n = 0
        Knapsack.available_items = []

        weight, value = result["weight"], result["value"]

        genetic = Genetic() if problem_type == 1 else UnboundedGenetic()

        Knapsack.n = 0
        Knapsack.available_items = []
        for i in range(n):
            Knapsack.add_item(weight=int(weight[i]), value=int(value[i]))

        def wrapper():
            for knapsack, y in genetic.evolution(lim=500):
                time.sleep(0.02)
                yield str(knapsack) + "\n"

            x = list(range(len(y)))
            plt.scatter(x, y)
            img = io.BytesIO()
            plt.savefig(img, format="png")
            img.seek(0)
            plt.close()

            encoded_img = base64.b64encode(img.read()).decode("utf-8")

            yield encoded_img

        response = Response(wrapper(), content_type="text/plain")
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
        # return Response(wrapper(), content_type="text/plain")

    except ValidationError as err:
        return jsonify(err.messages), 400
