from .start import reg_start_cmd
from .add import reg_add_cmd
from .emps import reg_emp_cmd
from .cur_month import reg_cur_month_cmd
from .export import reg_export_cmd
from .planb import reg_planb_cmd
from .settings import reg_settings
from .lmk_list import reg_lmk_list
from .whois import register_whois_handler

from .menu import reg_menu_cmd

def reg_commands(dp):
    reg_start_cmd(dp)
    register_whois_handler(dp)
    reg_add_cmd(dp)
    reg_emp_cmd(dp)
    reg_cur_month_cmd(dp)
    reg_export_cmd(dp)
    reg_planb_cmd(dp)
    reg_settings(dp)
    reg_lmk_list(dp)
    reg_menu_cmd(dp)