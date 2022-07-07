def is_ticket(data: str) -> bool:
	return data.startswith('ticket_')


def is_score(data: str) -> bool:
	return data.startswith('score_')