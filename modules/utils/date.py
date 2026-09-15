from datetime import date
from dateutil.relativedelta import relativedelta

def get_target_yyyymm(months_ago: int = 0) -> str:
    """
    Returns a string representing the year and month (YYYY-MM) that is 'months_ago' months before today.

    Args:
        months_ago (int): Number of months to subtract from the current date. Default is (Current month).

    Returns:
        str: Year and month in 'YYYY-MM' format.
    """
    target_date = date.today() - relativedelta(months = months_ago)
    return target_date.strftime('%Y-%m')

def get_months_start_n_months_ago(months_ago: int = 0) -> date:
    """
    Returns a date object representing the first day of the month that is 'months_ago' months before today.

    Args:
        months_ago (int): Number of months to subtract from the current month. Default is 0 (current month).

    Returns:
        date: The first day of the resulting month.
    """
    return date.today().replace(day=1) - relativedelta(months = months_ago)
