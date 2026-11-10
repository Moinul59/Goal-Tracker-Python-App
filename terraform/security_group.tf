resource "aws_security_group" "main" {
  name        = "goal-tracker-sg"
  vpc_id      = aws_vpc.main.id
  description = "Security Group for Goal Tracker App"

  tags = {
    Name = "goal-tracker-sg"
  }
}

resource "aws_security_group" "alb" {
  name        = "goal-tracker-alb-sg"
  vpc_id      = aws_vpc.main.id
  description = "Security Group for Goal Tracker App ALB"
  tags = {
    Name = "goal-tracker-alb-sg"
  }
}

resource "aws_security_group" "rds" {
  name        = "goal-tracker-rds-sg"
  vpc_id      = aws_vpc.main.id
  description = "Security Group for Goal Tracker App RDS"

  tags = {
    Name = "goal-tracker-rds-sg"
  }
}

resource "aws_security_group" "redis" {
  name        = "goal-tracker-redis-sg"
  vpc_id      = aws_vpc.main.id
  description = "Security Group for Goal Tracker App Redis"

  tags = {
    Name = "goal-tracker-redis-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb.id
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  to_port           = 443
}

resource "aws_vpc_security_group_ingress_rule" "ecs_from_alb" {
  security_group_id            = aws_security_group.main.id
  ip_protocol                  = "tcp"
  from_port                    = 8000
  to_port                      = 8000
  referenced_security_group_id = aws_security_group.alb.id
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_ecs" {
  security_group_id            = aws_security_group.rds.id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = aws_security_group.main.id
}

resource "aws_vpc_security_group_ingress_rule" "redis_from_ecs" {
  security_group_id            = aws_security_group.redis.id
  ip_protocol                  = "tcp"
  from_port                    = 6379
  to_port                      = 6379
  referenced_security_group_id = aws_security_group.main.id
}

resource "aws_vpc_security_group_egress_rule" "ecs_to_rds" {
  security_group_id            = aws_security_group.main.id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  referenced_security_group_id = aws_security_group.rds.id
}

resource "aws_vpc_security_group_egress_rule" "ecs_to_redis" {
  security_group_id            = aws_security_group.main.id
  ip_protocol                  = "tcp"
  from_port                    = 6379
  to_port                      = 6379
  referenced_security_group_id = aws_security_group.redis.id
}