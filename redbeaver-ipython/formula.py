from redbeaver.formula import Formula as RedbeaverFormula
import sympy
from IPython.display import display, Math
import re


class Formula(RedbeaverFormula):
    __LATEX_KEY__ = 3

    def _update_fn_registry(self, fn, wrapped_fn):
        super(Formula, self)._update_fn_registry(fn, wrapped_fn)

        self._fn_registry[fn.__name__] += (('latex', self._get_latex(fn.__name__)),)

    def _wrap_body(self, fn, num):
        ret = super(Formula, self)._wrap_body(fn, num)
        
        try:
            display(Math(self._get_fn_latex(fn.__name__)))
        except:
            display(self._get_fn_latex(fn.__name__))
        
        return ret

    def _get_latex(self, fn_name):
        for arg in self._get_fn_args(fn_name):
            locals().update({arg: sympy.Symbol(arg)})
            
        try:
            return '%s = %s' % (
                Formula._get_latex_fn_name(fn_name),
                sympy.latex(eval(self._get_fn_return_str(fn_name)))
            )
        except TypeError as e:
            return e.args
    
    @staticmethod
    def _get_latex_fn_name(fn_name):
        return fn_name.replace('__', '^')
    
    def _get_fn_return_str(self, fn_name):  
        try:
            return re.search('(?<=return)\s+.+', self._get_fn_src_str(fn_name)).group(0)
        except:
            return 'None'
    
    def _get_fn_src_str(self, fn_name):
        return self._get_fn_src(fn_name)[0][-1]
    
    def _get_fn_latex(self, fn_name):
        return self._fn_registry[fn_name][self.__LATEX_KEY__][1]
