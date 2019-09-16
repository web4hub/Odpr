from odpr_shared_models.serializers import \
	FilterPropertySerializer, \
	TagSerializer, \
	BadgeSerializer
from documentation.serializers import DocumentationTagSerializer

# Maps CreateSerializers with lists of filter functions. Note: an instance of each serializer is needed in order to work as key.
# A List for each value is needed instead of a single lambda.
serializer_reuse_filter_map = {
	FilterPropertySerializer(): [(lambda element: {'name': element['name']}), ],
	TagSerializer(): [(lambda element: {'tag': element['tag']}), ],
	DocumentationTagSerializer(): [(lambda element: {'tag': element['tag']}), ],
	BadgeSerializer(): [(lambda element: {'title': element['title']}), ],
	# Many models are not suited to be used for reusing already existing objects, those are not listed here.
	# e.g.:
	# FilterProperties, TextWithHistory, ReputationRule, BadgeRule, BadgeOwnership, Report, Comment, CommentRelationship,
	# ProfileImage, Notification, Scenery, SceneryImage, SceneryFile, SceneryRelationship, SceneryTagRelationship,
	# Request, RequestImage, RequestRelationship, RequestTagRelationship, Answer, AnswerRelationship, RequestFile
	# TODO: add more reuse filters for the nested creation if needed.
}
