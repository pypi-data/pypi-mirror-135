# rally-cly:Rally API Client

## Install

From code repo dir:

```shell
pip install --user --editable .
```

## Use
> RallyTypeGeneric class is used for all models with no specific model Class
```python
from typing import List
from rallycli import RallyAPI
from rallycli.models import RallyTypeGeneric, type_names, US, Feature, User

rally_api = RallyAPI(key_based_auth=True,
                     external_key="<your_external_key_here>",
                     baseurl="https://eu1.rallydev.com/",
                     workspace="/workspace/<workspace_OID_here>")

project_ref: str = "/project/<your_project_OID_here>"

## getting the project
project: RallyTypeGeneric = rally_api.project_api.get_project_by_ref(project_ref)
## getting project releases
releases: List[RallyTypeGeneric] = rally_api.timebox_api.get_releases_for_project(project_ref=project._ref)
## getting project iterations
iterations: List[RallyTypeGeneric] = rally_api.timebox_api.get_active_iterations_for_project(project_ref=project._ref)
## create UserStory
us: US = US()
us.Name = f"Autocreated Us {n}"
us.Project = project_ref
us.Description = f"Test US {n} para rallycli python module. By {rally_api.user_api.get_this_user().EmailAddress}"
us.Owner = rally_api.user_api.get_this_user()
us.Release = releases[0]._ref
us.Iteration = iterations[0]._ref

created_us: US = rally_api.artifact_api.create_artifact(us, type_names.US)
print(created_us)

feature: Feature = rally_api.artifact_api.get_artifact_by_formattedid("FE1")
print(feature.Name)

# Get all disabled users using 4 parallel threads
users: List[User] = rally_api.query("( Disabled = true)", "user", fetch="Username",model_class=User, 
                                    threads=4, pagesize=80)
```

