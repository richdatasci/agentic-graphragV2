variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "agentic-graphrag"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}
