from pydantic import BaseModel
# from pydantic import PyObjectId
# from pydantic import Field
# from pydantic import ConfigDict

# class PackageModel(BaseModel):
#     id: Optional[PyObjectId] = Field(alias="_id", default=None)
#     githuburl: str = Field(...)
#     model_config = ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True,
#         json_schema_extra={
#             "pkg:maven/androidx.arch.core/core-common": {
#                 "githuburl": "https://github.com/androidx/androidx",
#             }
#         },
#     )