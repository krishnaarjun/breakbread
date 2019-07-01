from breakbread.utils import send_html_mail
from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.contrib import rdb

logger = get_task_logger(__name__)


@shared_task
def email_on_potluck_publish(origin, group_info, user_info, guests=None):
    menu_link = origin + '/select-food/group/' + \
        group_info['id'] + '/user/' + user_info['id']
    context = {'group_info': group_info,
               'user_info': user_info, 'menu_link': menu_link}
    if guests:
        context['guests'] = guests
    # user_info['email']
    logger.info("Sending potluck publish mail")
    send_html_mail(subject='potluck is scheduled on 06-29-2019',
                   recipient_list=['saitejagoli0@gmail.com', ], html_template='potluck_publish.html', context=context)
    return 'Successfully mailed potluck info'
