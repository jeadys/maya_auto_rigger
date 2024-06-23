import maya.cmds as cmds

from modular.biped.biped import Segment
from modular.kinematics.ik_chain import IKChain
from modular.kinematics.fk_chain import FKChain
from modular.kinematics.skeleton import Skeleton
from modular.mechanisms.limb_stretch import Stretch

from typing import Literal


class Toe:

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.name = cmds.getAttr(f"{self.node}.component_type")
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=node, prefix=self.prefix)
        self.ik_chain: IKChain = IKChain(node=node, name=self.name, prefix=self.prefix)
        self.fk_chain: FKChain = FKChain(node=node, name=self.name, prefix=self.prefix)
        self.stretch: Stretch = Stretch(node=node, name=self.name, prefix=self.prefix)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(segments=self.segments)
        self.skeleton.orient_skeleton(segments=self.segments)

    def forward_kinematic(self) -> None:
        self.fk_joints = self.fk_chain.fk_joint(segments=self.segments[1:])
        self.fk_controls = self.fk_chain.fk_control(segments=self.segments[1:-1])

    def inverse_kinematic(self) -> None:
        self.ik_joints = self.ik_chain.ik_joint(segments=self.segments[1:])
        self.ik_controls = self.ik_chain.ik_control(segments=self.segments[1:])
        self.ik_chain.inverse_kinematic_space_swap(ik_control=self.ik_controls[0], pole_control=self.ik_controls[1])

    def switch_kinematic(self) -> None:
        self.ik_chain.switch_kinematic(fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def stretch_mechanism(self) -> None:
        self.stretch.stretch_joint(segments=self.segments[1:])
        self.stretch.stretch_attribute()
        self.stretch.stretch_node(segments=self.segments[1:])

    def generate_toe(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()

        if cmds.getAttr(f"{self.node}.stretch"):
            self.stretch_mechanism()
