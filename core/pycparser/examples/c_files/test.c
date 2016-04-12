set vul_type = "xss";
set vul_level = 1;
set vul_scope = "auditing";
set vul_choice = -1;
set vul = "test1";

#pragma test1

void entry() {
	test1.start('/');
}