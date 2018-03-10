def every_monday():
	current_votations = Votation.objects.filter(active=True)
	current_votations.update(active=False, finished=True)

	winners 		= winner_every_votation/category # And delete associated winners
	almost_winners	= # 3 most rated from every cat/vots and delete associations


	next_votations = create_next_votations()
	next_votations.update(active=True)

	next_votations = add_books_next_vots(next_votations)


def get_winners(votations):
	winners = {}

	for v in votations:
		winners[v.category.slug] = v.book_set.latest()
