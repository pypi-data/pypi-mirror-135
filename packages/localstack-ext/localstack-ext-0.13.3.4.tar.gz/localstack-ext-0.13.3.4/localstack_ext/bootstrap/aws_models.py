from localstack.utils.aws import aws_models
IeRTV=super
IeRTd=None
IeRTs=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IeRTV(LambdaLayer,self).__init__(arn)
  self.cwd=IeRTd
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IeRTs.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(RDSDatabase,self).__init__(IeRTs,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(RDSCluster,self).__init__(IeRTs,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(AppSyncAPI,self).__init__(IeRTs,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(AmplifyApp,self).__init__(IeRTs,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(ElastiCacheCluster,self).__init__(IeRTs,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(TransferServer,self).__init__(IeRTs,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(CloudFrontDistribution,self).__init__(IeRTs,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IeRTs,env=IeRTd):
  IeRTV(CodeCommitRepository,self).__init__(IeRTs,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
