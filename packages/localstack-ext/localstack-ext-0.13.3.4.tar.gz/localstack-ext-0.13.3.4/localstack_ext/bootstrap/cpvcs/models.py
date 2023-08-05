from datetime import datetime
rtmzS=str
rtmzD=int
rtmzU=super
rtmzi=False
rtmzy=isinstance
rtmzI=hash
rtmzO=bool
rtmzf=True
rtmzh=list
rtmzC=map
rtmzL=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:rtmzS):
  self.hash_ref:rtmzS=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={rtmzS(MAIN):API_STATES_DIR,rtmzS(DDB):DYNAMODB_DIR,rtmzS(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:rtmzS,rel_path:rtmzS,file_name:rtmzS,size:rtmzD,service:rtmzS,region:rtmzS,serialization:Serialization):
  rtmzU(StateFileRef,self).__init__(hash_ref)
  self.rel_path:rtmzS=rel_path
  self.file_name:rtmzS=file_name
  self.size:rtmzD=size
  self.service:rtmzS=service
  self.region:rtmzS=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return rtmzi
  if not rtmzy(other,StateFileRef):
   return rtmzi
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return rtmzI((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->rtmzO:
  if not other:
   return rtmzi
  if not rtmzy(other,StateFileRef):
   return rtmzi
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->rtmzO:
  for other in others:
   if self.congruent(other):
    return rtmzf
  return rtmzi
 def metadata(self)->rtmzS:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:rtmzS,state_files:Set[StateFileRef],parent_ptr:rtmzS):
  rtmzU(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:rtmzS=parent_ptr
 def state_files_info(self)->rtmzS:
  return "\n".join(rtmzh(rtmzC(lambda state_file:rtmzS(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:rtmzS,head_ptr:rtmzS,message:rtmzS,timestamp:rtmzS=rtmzS(datetime.now().timestamp()),delta_log_ptr:rtmzS=rtmzL):
  self.tail_ptr:rtmzS=tail_ptr
  self.head_ptr:rtmzS=head_ptr
  self.message:rtmzS=message
  self.timestamp:rtmzS=timestamp
  self.delta_log_ptr:rtmzS=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:rtmzS,to_node:rtmzS)->rtmzS:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:rtmzS,state_files:Set[StateFileRef],parent_ptr:rtmzS,creator:rtmzS,rid:rtmzS,revision_number:rtmzD,assoc_commit:Commit=rtmzL):
  rtmzU(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:rtmzS=creator
  self.rid:rtmzS=rid
  self.revision_number:rtmzD=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(rtmzC(lambda state_file:rtmzS(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:rtmzS,state_files:Set[StateFileRef],parent_ptr:rtmzS,creator:rtmzS,comment:rtmzS,active_revision_ptr:rtmzS,outgoing_revision_ptrs:Set[rtmzS],incoming_revision_ptr:rtmzS,version_number:rtmzD):
  rtmzU(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(rtmzC(lambda stat_file:rtmzS(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
