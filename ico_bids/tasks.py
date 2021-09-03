from datetime import datetime
from django.db.models import Q, Sum
from ico.celery import app
from ico_bids.models import Bid, Token

@app.task()
def allocate_token():
    curr_time = datetime.now().time()

    token_qs = (
        Token.objects
        .filter(end_time__lt=curr_time)
    )

    status_names = [status[0] for status in Bid.STATUS]

    for token in token_qs:
        token_available = token.available_token

        bids = (
            Bid.objects
            .filter(
                token=token,
                created_at__time__range=(token.start_time,token.end_time),
                status='PENDING',
            )
            .order_by('-bid_price', 'created_at')
        )

        prices = [bid.bid_price for bid in bids.distinct('bid_price')]
        for price in prices:
            curr_qs = bids.filter(bid_price=price)

            if not token_available:
                for obj in curr_qs:
                    obj.alloted_tokens = 0
                    obj.status = status_names[1]
                Bid.objects.bulk_update(curr_qs,['alloted_tokens', 'status'])
                continue

            required_token = sum([curr.number_of_token for curr in curr_qs])

            if required_token <= token_available:
                for obj in curr_qs:
                    obj.alloted_tokens = obj.number_of_token
                    obj.status = status_names[0]

                Bid.objects.bulk_update(curr_qs,['alloted_tokens', 'status'])
                token_available = token_available - required_token
            else:
                while token_available:
                    temp_qs = curr_qs.filter(status='PENDING')
                    if not temp_qs:
                        break

                    min_available = token_available // len(temp_qs)
                    if min_available:
                        for obj in temp_qs:
                            token_needed = obj.number_of_token - obj.alloted_tokens
                            if token_needed <= min_available:
                                obj.alloted_tokens += token_needed
                                obj.status = status_names[0]
                                token_available -= token_needed
                            else:
                                obj.alloted_tokens += min_available
                                token_available -= min_available

                        if not token_available:
                            for obj in temp_qs:
                                if obj.alloted_tokens:
                                    obj.status = status_names[0]
                                else:
                                    obj.status = status_names[1]

                        Bid.objects.bulk_update(
                            temp_qs,['alloted_tokens', 'status']
                        )
                    else:
                        for obj in temp_qs:
                            if token_available:
                                obj.alloted_tokens += 1
                                token_available -= 1
                            if obj.alloted_tokens:
                                obj.status = status_names[0]
                            else:
                                obj.status = status_names[1]

                        Bid.objects.bulk_update(
                            temp_qs,['alloted_tokens', 'status']
                        )

        print(f'Allocation done for {token.name}')
    print(f'Allocation for all the tokens is completed')
