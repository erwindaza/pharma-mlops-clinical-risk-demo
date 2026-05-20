locals {
  name_prefix = substr(replace(var.project_name, "_", "-"), 0, 32)
}
