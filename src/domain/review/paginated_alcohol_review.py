from src.domain.review import Review
from src.domain.review.paginated_review import PaginatedReview


class PaginatedAlcoholReview(PaginatedReview):
    my_review: Review | None
