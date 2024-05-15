from app.telegram.handlers.commands.start import reg_start_cmd
from app.telegram.handlers.commands.add import reg_add_cmd
from app.telegram.handlers.commands.emps import reg_emp_cmd
from app.telegram.handlers.commands.cur_month import reg_cur_month_cmd


def reg_commands(dp):
    reg_start_cmd(dp)
    reg_add_cmd(dp)
    reg_emp_cmd(dp)
    reg_cur_month_cmd(dp)