provider "google" {
  project = "t-replica-430811-r5"
  region  = "europe-west3"  # Change to your preferred region
}

resource "google_container_cluster" "primary" {
  name     = "my-gke-cluster"
  location = "europe-west3-a"  # This is the zone where the control plane (master node) will be located.

  # Cluster-level settings
  initial_node_count = 1  # This is just a placeholder as we'll define our own node pools.

  # Remove the default node pool that is automatically created
  remove_default_node_pool = true

  # Optionally, you can specify network, subnetwork, and other settings here.
  deletion_protection = false  # Disable deletion protection
}

# Create a node pool for worker nodes in zone us-central1-b
resource "google_container_node_pool" "worker_pool_1" {
  name       = "worker-pool-1"
  cluster    = google_container_cluster.primary.name
  location   = "europe-west3-a"  # This refers to the master node's location

  node_config {
    machine_type = "e2-micro"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  node_count = 1

  # Specify the zones where this node pool should be deployed
  node_locations = ["europe-west3-b"]
}

# Create a node pool for worker nodes in zone us-central1-c
resource "google_container_node_pool" "worker_pool_2" {
  name       = "worker-pool-2"
  cluster    = google_container_cluster.primary.name
  location   = "europe-west3-a"  # This refers to the master node's location

  node_config {
    machine_type = "e2-micro"
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  node_count = 1

  # Specify the zones where this node pool should be deployed
  node_locations = ["europe-west3-c"]
}

output "kubernetes_cluster_name" {
  value = google_container_cluster.primary.name
}

output "kubernetes_cluster_endpoint" {
  value = google_container_cluster.primary.endpoint
}

output "kubernetes_cluster_master_version" {
  value = google_container_cluster.primary.master_version
}

# For executing
# terraform init
# terraform validate
# terraform plan -out=tfplan
# terraform apply "tfplan"
