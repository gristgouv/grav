resource "kubernetes_service_v1" "grav" {
  metadata {
    name      = "grav"
    namespace = "grist"
  }
  spec {
    selector = {
      "app.kubernetes.io/name"     = "grav"
      "app.kubernetes.io/instance" = "grav"
    }
    port {
      port        = 80
      target_port = 80
    }
  }
}
resource "kubernetes_ingress_v1" "grav" {
  metadata {
    namespace = "grist"
    name      = "grav"
    annotations = {
      "nginx.ingress.kubernetes.io/use-regex" = true
    }
  }
  spec {
    tls {
      hosts       = ["grist.minikube.local"]
      secret_name = "grist-tls"
    }
    rule {
      host = "grist.minikube.local"
      http {
        path {
          path      = "/(o/[^/]+/)?api/docs/[^/]+/attachments$"
          path_type = "ImplementationSpecific"
          backend {
            service {
              name = "grav"
              port {
                number = 80
              }
            }
          }
        }
        path {
          path      = "/dw/[^/]+/v/[^/]+/o/[^/]+/uploads$"
          path_type = "ImplementationSpecific"
          backend {
            service {
              name = "grav"
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}
resource "kubernetes_deployment_v1" "grav" {
  metadata {
    namespace = "grist"
    name      = "grav"
  }
  spec {
    selector {
      match_labels = {
        "app.kubernetes.io/name"     = "grav"
        "app.kubernetes.io/instance" = "grav"
      }
    }
    template {
      metadata {
        labels = {
          "app.kubernetes.io/name"     = "grav"
          "app.kubernetes.io/instance" = "grav"
        }
      }
      spec {
        container {
          image   = "python:3.13"
          name    = "grav"
          command = ["sleep"]
          args    = ["infinity"]
          volume_mount {
            name       = "grav"
            mount_path = "/grav"
          }
          port {
            protocol       = "TCP"
            name           = "http"
            container_port = "80"
          }
        }
        volume {
          name = "grav"
          host_path {
            path = "/grav"
          }
        }
      }
    }
  }
}
