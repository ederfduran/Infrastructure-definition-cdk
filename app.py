
from aws_cdk import core
from stacks.vpc_stack import VPCStack
from stacks.security_stack import SecurityStack

app = core.App()
# vpc = CF stack name
vpc_stack = VPCStack(app, 'vpc')
security_stack = SecurityStack(app, 'security-stack', vpc=vpc_stack.vpc)

app.synth()