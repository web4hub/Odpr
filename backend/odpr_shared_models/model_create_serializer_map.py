from .serializers import TextWithHistorySerializer,\
	FilterPropertySerializer, \
	TagSerializer, \
	FilterPropertiesSerializer, \
	ReputationRuleSerializer, \
	BadgeSerializer, \
	BadgeRuleSerializer, \
	BadgeOwnershipSerializer, \
	ReportSerializer, \
	CommentSerializer, \
	CommentRelationshipSerializer, \
	ProfileImageSerializer, \
	NotificationSerializer, \
	ImageSerializer, \
	FileSerializer
from documentation.serializers import DocumentationTagSerializer, DocumentationFileSerializer
from sceneries.serializers import ScenerySerializer, \
	SceneryImageSerializer, \
	SceneryFileSerializer, \
	SceneryRelationshipSerializer, \
	SceneryTagRelationshipSerializer
from scenery_requests.serializers import RequestSerializer, \
	RequestImageSerializer, \
	RequestRelationshipSerializer, \
	RequestTagRelationshipSerializer, \
	AnswerSerializer, \
	AnswerRelationshipSerializer, \
	RequestFileSerializer

model_create_serializer_map = {
	'TextWithHistory': TextWithHistorySerializer,
	'FilterProperty': FilterPropertySerializer,
	'FilterProperties': FilterPropertiesSerializer,
	'Tag': TagSerializer,
	'DocumentationTag': DocumentationTagSerializer,
	'ReputationRule': ReputationRuleSerializer,
	'Badge': BadgeSerializer,
	'BadgeRule': BadgeRuleSerializer,
	'BadgeOwnership': BadgeOwnershipSerializer,
	'Report': ReportSerializer,
	'Comment': CommentSerializer,
	'CommentRelationship': CommentRelationshipSerializer,
	'ProfileImage': ProfileImageSerializer,
	'Notification': NotificationSerializer,
	'Scenery': ScenerySerializer,
	'SceneryRelationship': SceneryRelationshipSerializer,
	'SceneryTagRelationship': SceneryTagRelationshipSerializer,
	'SceneryImage': SceneryImageSerializer,
	'SceneryFile': SceneryFileSerializer,
	'Request': RequestSerializer,
	'RequestImage': RequestImageSerializer,
	'RequestRelationship': RequestRelationshipSerializer,
	'RequestTagRelationship': RequestTagRelationshipSerializer,
	'Answer': AnswerSerializer,
	'AnswerRelationship': AnswerRelationshipSerializer,
	'RequestFile': RequestFileSerializer,
	'DocumentationFile': DocumentationFileSerializer,
	'Image': ImageSerializer,
	'File': FileSerializer,

	# TODO: add more serializers for the nested creation.
}
