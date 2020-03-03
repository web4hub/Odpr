POST,\
	SCENERY_POST, REQUEST_POST, ANSWER_POST, DOCUMENTATION_POST,\
	VOTE,\
	UPVOTE,\
	DOWNVOTE,\
	STAR,\
	UNVOTE,\
	UNSTAR,\
	SCENERY_UPVOTE, SCENERY_DOWNVOTE, SCENERY_STAR, SCENERY_UNVOTE, SCENERY_UNSTAR,\
	REQUEST_UPVOTE, REQUEST_DOWNVOTE, REQUEST_STAR, REQUEST_UNVOTE, REQUEST_UNSTAR,\
	ANSWER_UPVOTE, ANSWER_DOWNVOTE, ANSWER_UNVOTE,\
	COMMENT_UPVOTE, COMMENT_DOWNVOTE, COMMENT_UNVOTE,\
	COMMENT,\
	DOWNLOAD,\
	FOLLOW,\
	BLOCK,\
	REPORT,\
	SCENERY_REPORT, REQUEST_REPORT, USER_REPORT, ANSWER_REPORT, COMMENT_REPORT, DOCUMENTATION_REPORT,\
	EARNED_POINTS = range(0, 39)

Actions = (
	(POST, 'Posted Content'),
	(SCENERY_POST, 'Posted Scenery'),
	(REQUEST_POST, 'Posted Request'),
	(ANSWER_POST, 'Posted Answer to a Request'),
	(DOCUMENTATION_POST, 'Posted Documentation/Tutorial'),
	(VOTE, 'Voted'),
	(UPVOTE, 'Upvote'),
	(DOWNVOTE, 'Downvote'),
	(STAR, 'Starred'),
	(UNVOTE, 'Unvoted'),
	(UNSTAR, 'Unstarred'),
	(SCENERY_UPVOTE, 'Upvoted Scenery'),
	(SCENERY_DOWNVOTE, 'Downvoted Scenery'),
	(SCENERY_STAR, 'Starred Scenery'),
	(SCENERY_UNVOTE, 'Unvoted Scenery'),
	(SCENERY_UNSTAR, 'Unstarred Scenery'),
	(REQUEST_UPVOTE, 'Upvoted Request'),
	(REQUEST_DOWNVOTE, 'Downvoted Request'),
	(REQUEST_STAR, 'Starred Request'),
	(REQUEST_UNVOTE, 'Unvoted Request'),
	(REQUEST_UNSTAR, 'Unstarred Request'),
	(COMMENT_UPVOTE, 'Upvoted Comment'),
	(COMMENT_DOWNVOTE, 'Downvoted Comment'),
	(COMMENT_UNVOTE, 'Unvoted Comment'),
	(COMMENT, 'Posted Comment'),
	(DOWNLOAD, 'Download'),
	(FOLLOW, 'Follow'),
	(BLOCK, 'Blockage'),
	(REPORT, 'Report'),
	(SCENERY_REPORT, 'Reported Scenery'),
	(REQUEST_REPORT, 'Reported Request'),
	(USER_REPORT, 'Reported User'),
	(ANSWER_REPORT, 'Reported Answer'),
	(COMMENT_REPORT, 'Reported Comment'),
	(DOCUMENTATION_REPORT, 'Reported Documentation'),
	(EARNED_POINTS, 'Earned Points'),
)
