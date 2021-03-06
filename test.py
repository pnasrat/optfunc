import unittest
import optfunc
from StringIO import StringIO

class TestOptFunc(unittest.TestCase):
    def test_three_positional_args(self):
        
        has_run = [False]
        def func(one, two, three):
            has_run[0] = True
        
        # Should only have the -h help option
        parser, required_args = optfunc.func_to_optionparser(func)
        self.assertEqual(len(parser.option_list), 1)
        self.assertEqual(str(parser.option_list[0]), '-h/--help')
        
        # Should have three required args
        self.assertEqual(required_args, ['one', 'two', 'three'])
        
        # Running it with the wrong number of arguments should cause an error
        for argv in (
            ['one'],
            ['one', 'two'],
            ['one', 'two', 'three', 'four'],
        ):
            e = StringIO()
            optfunc.run(func, argv, stderr=e)
            self.assert_('Required 3 arguments' in e.getvalue(), e.getvalue())
            self.assertEqual(has_run[0], False)
        
        # Running it with the right number of arguments should be fine
        e = StringIO()
        optfunc.run(func, ['one', 'two', 'three'], stderr=e)
        self.assertEqual(e.getvalue(), '')
        self.assertEqual(has_run[0], True)
    
    def test_one_arg_one_option(self):
        
        has_run = [False]
        def func(one, option=''):
            has_run[0] = (one, option)
        
        # Should have -o option as well as -h option
        parser, required_args = optfunc.func_to_optionparser(func)
        self.assertEqual(len(parser.option_list), 2)
        strs = [str(o) for o in parser.option_list]
        self.assert_('-h/--help' in strs)
        self.assert_('-o/--option' in strs)
        
        # Should have one required arg
        self.assertEqual(required_args, ['one'])
        
        # Should execute
        self.assert_(not has_run[0])
        optfunc.run(func, ['the-required', '-o', 'the-option'])
        self.assert_(has_run[0])
        self.assertEqual(has_run[0], ('the-required', 'the-option'))
        
        # Option should be optional
        has_run[0] = False
        optfunc.run(func, ['required2'])
        self.assert_(has_run[0])
        self.assertEqual(has_run[0], ('required2', ''))
    
    def test_options_are_correctly_named(self):
        def func1(one, option='', verbose=False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func1)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-o/--option', '-v/--verbose'])
    
    def test_option_with_hyphens(self):
        def func2(option_with_hyphens=True):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func2)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-o/--option-with-hyphens'])
    
    def test_options_with_same_inital_use_next_letter(self):
        def func1(one, version='', verbose=False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func1)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-v/--version', '-e/--verbose'])
    
    def test_short_option_can_be_named_explicitly(self):
        def func1(one, option='', q_verbose=False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(func1)
        strs = [str(o) for o in parser.option_list]
        self.assertEqual(strs, ['-h/--help', '-o/--option', '-q/--verbose'])
    
    def test_notstrict(self):
        "@notstrict tells optfunc to tolerate missing required arguments"
        def strict_func(one):
            pass
        
        e = StringIO()
        optfunc.run(strict_func, [], stderr=e)
        self.assertEqual(e.getvalue().strip(), 'Required 1 arguments, got 0')
        
        @optfunc.notstrict
        def notstrict_func(one):
            pass
        
        e = StringIO()
        optfunc.run(notstrict_func, [], stderr=e)
        self.assertEqual(e.getvalue().strip(), '')
    
    def test_arghelp(self):
        "@arghelp('foo', 'help about foo') sets help text for parameters"
        @optfunc.arghelp('foo', 'help about foo')
        def foo(foo = False):
            pass
        
        parser, required_args = optfunc.func_to_optionparser(foo)
        opt = parser.option_list[1]
        self.assertEqual(str(opt), '-f/--foo')
        self.assertEqual(opt.help, 'help about foo')

if __name__ == '__main__':
    unittest.main()
