# quicksort algorithm here
def sort(queryset):
    less, equal, greater = [], [], []

    if len(queryset) < 2:
        return queryset
    else:
        pivot = queryset[0]
        for x in queryset:
            if x.id < pivot.id:
                less.append(x)
            if x.id == pivot.id:
                equal.append(x)
            if x.id > pivot.id:
                greater.append(x)
        return sort(less) + equal + sort(greater)
