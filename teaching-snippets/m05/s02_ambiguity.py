# A boundary needs policies for conversion, missing values, explicit nulls,
# and unexpected fields. Convenient coercion may accept unintended data;
# strictness is a deliberate choice rather than a universal requirement.
#
# Compare a coercing quantity model with a stricter order input policy.

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class CoercingItem(BaseModel):
    quantity: int


class StrictItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    quantity: int = Field(strict=True, gt=0)
    note: str | None = None          # Optional and nullable are separate choices.


print(CoercingItem(quantity="2").quantity)  # Converted to integer 2.
omitted_note = StrictItem(quantity=2)
explicit_null = StrictItem(quantity=2, note=None)
print(omitted_note.model_fields_set)  # {'quantity'}
print(explicit_null.model_fields_set) # {'quantity', 'note'}

for payload in [{"quantity": "2"}, {"quantity": 2, "discount": 99}]:
    try:
        StrictItem.model_validate(payload)
    except ValidationError as error:
        print(error.errors()[0]["type"])
# A nullable field without a default can still be required.
