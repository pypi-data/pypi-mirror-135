from __future__ import annotations
import photonvision._photonvision
import typing
import _pyntcore._ntcore
import wpimath.geometry._geometry

__all__ = [
    "LEDMode",
    "Packet",
    "PhotonCamera",
    "PhotonPipelineResult",
    "PhotonTrackedTarget",
    "PhotonUtils",
    "SimPhotonCamera",
    "SimVisionSystem",
    "SimVisionTarget"
]


class LEDMode():
    """
    Members:

      kDefault

      kOff

      kOn

      kBlink
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'kDefault': <LEDMode.kDefault: -1>, 'kOff': <LEDMode.kOff: 0>, 'kOn': <LEDMode.kOn: 1>, 'kBlink': <LEDMode.kBlink: 2>}
    kBlink: photonvision._photonvision.LEDMode # value = <LEDMode.kBlink: 2>
    kDefault: photonvision._photonvision.LEDMode # value = <LEDMode.kDefault: -1>
    kOff: photonvision._photonvision.LEDMode # value = <LEDMode.kOff: 0>
    kOn: photonvision._photonvision.LEDMode # value = <LEDMode.kOn: 1>
    pass
class Packet():
    """
    A packet that holds byte-packed data to be sent over NetworkTables.
    """
    def __eq__(self, arg0: Packet) -> bool: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs an empty packet.

        Constructs a packet with the given data.

        :param data: The packet data.
        """
    @typing.overload
    def __init__(self, data: typing.List[str]) -> None: ...
    def __ne__(self, arg0: Packet) -> bool: ...
    def clear(self) -> None: 
        """
        Clears the packet and resets the read and write positions.
        """
    def getData(self) -> typing.List[str]: 
        """
        Returns the packet data.

        :returns: The packet data.
        """
    def getDataSize(self) -> int: 
        """
        Returns the number of bytes in the data.

        :returns: The number of bytes in the data.
        """
    __hash__ = None
    pass
class PhotonCamera():
    """
    Represents a camera that is connected to PhotonVision.ß
    """
    @typing.overload
    def __init__(self, cameraName: str) -> None: 
        """
        Constructs a PhotonCamera from a root table.

        :param rootTable: The root table that the camera is broadcasting information
                          over.

        Constructs a PhotonCamera from the name of the camera.

        :param cameraName: The nickname of the camera (found in the PhotonVision
                           UI).
        """
    @typing.overload
    def __init__(self, rootTable: _pyntcore._ntcore.NetworkTable) -> None: ...
    def getDriverMode(self) -> bool: 
        """
        Returns whether the camera is in driver mode.

        :returns: Whether the camera is in driver mode.
        """
    def getLEDMode(self) -> LEDMode: 
        """
        Returns the current LED mode.

        :returns: The current LED mode.
        """
    def getLatestResult(self) -> PhotonPipelineResult: 
        """
        Returns the latest pipeline result.

        :returns: The latest pipeline result.
        """
    def getPipelineIndex(self) -> int: 
        """
        Returns the active pipeline index.

        :returns: The active pipeline index.
        """
    def hasTargets(self) -> bool: ...
    def setDriverMode(self, driverMode: bool) -> None: 
        """
        Toggles driver mode.

        :param driverMode: Whether to set driver mode.
        """
    def setLEDMode(self, led: LEDMode) -> None: 
        """
        Sets the LED mode.

        :param led: The mode to set to.
        """
    def setPipelineIndex(self, index: int) -> None: 
        """
        Allows the user to select the active pipeline index.

        :param index: The active pipeline index.
        """
    def takeInputSnapshot(self) -> None: 
        """
        Request the camera to save a new image file from the input
        camera stream with overlays.
        Images take up space in the filesystem of the PhotonCamera.
        Calling it frequently will fill up disk space and eventually
        cause the system to stop working.
        Clear out images in /opt/photonvision/photonvision_config/imgSaves
        frequently to prevent issues.
        """
    def takeOutputSnapshot(self) -> None: 
        """
        Request the camera to save a new image file from the output
        stream with overlays.
        Images take up space in the filesystem of the PhotonCamera.
        Calling it frequently will fill up disk space and eventually
        cause the system to stop working.
        Clear out images in /opt/photonvision/photonvision_config/imgSaves
        frequently to prevent issues.
        """
    pass
class PhotonPipelineResult():
    """
    Represents a pipeline result from a PhotonCamera.
    """
    def __eq__(self, arg0: PhotonPipelineResult) -> bool: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs an empty pipeline result.

        Constructs a pipeline result.

        :param latency: The latency in the pipeline.
        :param targets: The list of targets identified by the pipeline.
        """
    @typing.overload
    def __init__(self, latency: seconds, targets: typing.List[PhotonTrackedTarget]) -> None: ...
    def __ne__(self, arg0: PhotonPipelineResult) -> bool: ...
    def getBestTarget(self) -> PhotonTrackedTarget: 
        """
        Returns the best target in this pipeline result. If there are no targets,
        this method will return an empty target with all values set to zero. The
        best target is determined by the target sort mode in the PhotonVision UI.

        :returns: The best target of the pipeline result.
        """
    def getLatency(self) -> seconds: 
        """
        Returns the latency in the pipeline.

        :returns: The latency in the pipeline.
        """
    def getTargets(self) -> typing.List[PhotonTrackedTarget]: 
        """
        Returns a reference to the vector of targets.

        :returns: A reference to the vector of targets.
        """
    def hasTargets(self) -> bool: 
        """
        Returns whether the pipeline has targets.

        :returns: Whether the pipeline has targets.
        """
    __hash__ = None
    pass
class PhotonTrackedTarget():
    """
    Represents a tracked target within a pipeline.
    """
    def __eq__(self, arg0: PhotonTrackedTarget) -> bool: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs an empty target.

        Constructs a target.

        :param yaw:   The yaw of the target.
        :param pitch: The pitch of the target.
        :param area:  The area of the target.
        :param skew:  The skew of the target.
        :param pose:  The camera-relative pose of the target.
                      @Param corners The corners of the bounding rectangle.
        """
    @typing.overload
    def __init__(self, yaw: float, pitch: float, area: float, skew: float, pose: wpimath.geometry._geometry.Transform2d, corners: typing.List[typing.Tuple[float, float]]) -> None: ...
    def __ne__(self, arg0: PhotonTrackedTarget) -> bool: ...
    def getArea(self) -> float: 
        """
        Returns the target area (0-100).

        :returns: The target area.
        """
    def getCameraRelativePose(self) -> wpimath.geometry._geometry.Transform2d: 
        """
        Returns the pose of the target relative to the robot.

        :returns: The pose of the target relative to the robot.
        """
    def getCorners(self) -> typing.List[typing.Tuple[float, float]]: 
        """
        Returns the corners of the minimum area rectangle bounding this target.
        """
    def getPitch(self) -> float: 
        """
        Returns the target pitch (positive-up)

        :returns: The target pitch.
        """
    def getSkew(self) -> float: 
        """
        Returns the target skew (counter-clockwise positive).

        :returns: The target skew.
        """
    def getYaw(self) -> float: 
        """
        Returns the target yaw (positive-left).

        :returns: The target yaw.
        """
    __hash__ = None
    pass
class PhotonUtils():
    def __init__(self) -> None: ...
    @staticmethod
    def calculateDistanceToTarget(cameraHeight: meters, targetHeight: meters, cameraPitch: radians, targetPitch: radians) -> meters: 
        """
        Algorithm from
        https://docs.limelightvision.io/en/latest/cs_estimating_distance.html
        Estimates range to a target using the target's elevation. This method can
        produce more stable results than SolvePNP when well tuned, if the full 6d
        robot pose is not required.

        :param cameraHeight: The height of the camera off the floor.
        :param targetHeight: The height of the target off the floor.
        :param cameraPitch:  The pitch of the camera from the horizontal plane.
                             Positive valueBytes up.
        :param targetPitch:  The pitch of the target in the camera's lens. Positive
                             values up.

        :returns: The estimated distance to the target.
        """
    @staticmethod
    def estimateCameraToTarget(cameraToTargetTranslation: wpimath.geometry._geometry.Translation2d, fieldToTarget: wpimath.geometry._geometry.Pose2d, gyroAngle: wpimath.geometry._geometry.Rotation2d) -> wpimath.geometry._geometry.Transform2d: 
        """
        Estimates a {@link frc::Transform2d} that maps the camera position to the
        target position, using the robot's gyro. Note that the gyro angle provided
        *must* line up with the field coordinate system -- that is, it should read
        zero degrees when pointed towards the opposing alliance station, and
        increase as the robot rotates CCW.

        :param cameraToTargetTranslation: A Translation2d that encodes the x/y
                                          position of the target relative to the
                                          camera.
        :param fieldToTarget:             A frc::Pose2d representing the target
                                          position in the field coordinate system.
        :param gyroAngle:                 The current robot gyro angle, likely from
                                          odometry.

        :returns: A frc::Transform2d that takes us from the camera to the target.
        """
    @staticmethod
    def estimateCameraToTargetTranslation(targetDistance: meters, yaw: wpimath.geometry._geometry.Rotation2d) -> wpimath.geometry._geometry.Translation2d: 
        """
        Estimate the Translation2d of the target relative to the camera.

        :param targetDistance: The distance to the target.
        :param yaw:            The observed yaw of the target.

        :returns: The target's camera-relative translation.
        """
    @staticmethod
    def estimateFieldToCamera(cameraToTarget: wpimath.geometry._geometry.Transform2d, fieldToTarget: wpimath.geometry._geometry.Pose2d) -> wpimath.geometry._geometry.Pose2d: 
        """
        Estimates the pose of the camera in the field coordinate system, given the
        position of the target relative to the camera, and the target relative to
        the field. This *only* tracks the position of the camera, not the position
        of the robot itself.

        :param cameraToTarget: The position of the target relative to the camera.
        :param fieldToTarget:  The position of the target in the field.

        :returns: The position of the camera in the field.
        """
    @staticmethod
    @typing.overload
    def estimateFieldToRobot(cameraHeight: meters, targetHeight: meters, cameraPitch: radians, targetPitch: radians, targetYaw: wpimath.geometry._geometry.Rotation2d, gyroAngle: wpimath.geometry._geometry.Rotation2d, fieldToTarget: wpimath.geometry._geometry.Pose2d, cameraToRobot: wpimath.geometry._geometry.Transform2d) -> wpimath.geometry._geometry.Pose2d: 
        """
        Estimate the position of the robot in the field.

        :param cameraHeightMeters: The physical height of the camera off the floor
                                   in meters.
        :param targetHeightMeters: The physical height of the target off the floor
                                   in meters. This should be the height of whatever is being targeted (i.e. if
                                   the targeting region is set to top, this should be the height of the top of
                                   the target).
        :param cameraPitchRadians: The pitch of the camera from the horizontal plane
                                   in radians. Positive values up.
        :param targetPitchRadians: The pitch of the target in the camera's lens in
                                   radians. Positive values up.
        :param targetYaw:          The observed yaw of the target. Note that this
                                   *must* be CCW-positive, and Photon returns
                                   CW-positive.
        :param gyroAngle:          The current robot gyro angle, likely from
                                   odometry.
        :param fieldToTarget:      A frc::Pose2d representing the target position in
                                   the field coordinate system.
        :param cameraToRobot:      The position of the robot relative to the camera.
                                   If the camera was mounted 3 inches behind the
                                   "origin" (usually physical center) of the robot,
                                   this would be frc::Transform2d(3 inches, 0
                                   inches, 0 degrees).

        :returns: The position of the robot in the field.

        Estimates the pose of the robot in the field coordinate system, given the
        position of the target relative to the camera, the target relative to the
        field, and the robot relative to the camera.

        :param cameraToTarget: The position of the target relative to the camera.
        :param fieldToTarget:  The position of the target in the field.
        :param cameraToRobot:  The position of the robot relative to the camera. If
                               the camera was mounted 3 inches behind the "origin"
                               (usually physical center) of the robot, this would be
                               frc::Transform2d(3 inches, 0 inches, 0 degrees).

        :returns: The position of the robot in the field.
        """
    @staticmethod
    @typing.overload
    def estimateFieldToRobot(cameraToTarget: wpimath.geometry._geometry.Transform2d, fieldToTarget: wpimath.geometry._geometry.Pose2d, cameraToRobot: wpimath.geometry._geometry.Transform2d) -> wpimath.geometry._geometry.Pose2d: ...
    pass
class SimPhotonCamera(PhotonCamera):
    """
    Represents a camera that is connected to PhotonVision.ß
    """
    @typing.overload
    def __init__(self, cameraName: str) -> None: 
        """
        Constructs a Simulated PhotonCamera from a root table.

        :param rootTable: The root table that the camera is broadcasting information
                          over.

        Constructs a Simulated PhotonCamera from the name of the camera.

        :param cameraName: The nickname of the camera (found in the PhotonVision
                           UI).
        """
    @typing.overload
    def __init__(self, rootTable: _pyntcore._ntcore.NetworkTable) -> None: ...
    def submitProcessedFrame(self, latency: seconds, tgtList: typing.List[PhotonTrackedTarget]) -> None: 
        """
        Simulate one processed frame of vision data, putting one result to NT.

        :param latency: Latency of frame processing
        :param tgtList: Set of targets detected
        """
    pass
class SimVisionSystem():
    """
    Represents a camera that is connected to PhotonVision.
    """
    def __init__(self, name: str, camDiagFOV: degrees, camPitch: degrees, cameraToRobot: wpimath.geometry._geometry.Transform2d, cameraHeightOffGround: meters, maxLEDRange: meters, cameraResWidth: int, cameraResHeight: int, minTargetArea: float) -> None: ...
    def addSimVisionTarget(self, tgt: SimVisionTarget) -> None: ...
    def moveCamera(self, newcameraToRobot: wpimath.geometry._geometry.Transform2d, newCamHeight: meters, newCamPitch: degrees) -> None: ...
    def processFrame(self, robotPose: wpimath.geometry._geometry.Pose2d) -> None: ...
    @property
    def cam(self) -> SimPhotonCamera:
        """
        :type: SimPhotonCamera
        """
    pass
class SimVisionTarget():
    """
    Represents a target on the field which the vision processing system could
    detect.
    """
    def __init__(self, targetPos: wpimath.geometry._geometry.Pose2d, targetHeightAboveGround: meters, targetWidth: meters, targetHeight: meters) -> None: ...
    @property
    def targetHeight(self) -> meters:
        """
        :type: meters
        """
    @property
    def targetHeightAboveGround(self) -> meters:
        """
        :type: meters
        """
    @property
    def targetPos(self) -> wpimath.geometry._geometry.Pose2d:
        """
        :type: wpimath.geometry._geometry.Pose2d
        """
    @property
    def targetWidth(self) -> meters:
        """
        :type: meters
        """
    @property
    def tgtArea(self) -> square_meters:
        """
        :type: square_meters
        """
    pass
