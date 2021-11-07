# devops-netology
# Oleg Kirsanov

В результате применения файла [root of project]/terraform/.gitignore будут игнорироваться следующие файлы и директории:
# все директории ".terraform" на любом уровне вложенности
**/.terraform/*

# файлы оканчивающиеся .tfstate в корне проекта
*.tfstate
*.tfstate.*

# файл crash.log в корне проекта
crash.log
# Файлы оканчивающиеся на .tfvars в корне проекта
*.tfvars

# override files (используются локально), игнорируем при их расположении в корне проекта
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# CLI configuration files - игнорируем в корне проекта
.terraformrc
terraform.rc
New line
