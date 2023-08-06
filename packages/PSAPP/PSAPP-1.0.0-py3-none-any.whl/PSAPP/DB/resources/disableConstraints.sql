BEGIN
for i IN (select table_name, constraint_name
from ALL_CONSTRAINTS
where constraint_type ='R' and owner='_USER_'
and status = 'ENABLED')
loop
EXECUTE IMMEDIATE 'alter table _USER_.' ||i.table_name|| ' disable NOVALIDATE constraint ' ||i.constraint_name;
end loop i;

for i IN (select table_name, constraint_name
from ALL_CONSTRAINTS
where status = 'ENABLED' and owner='_USER_' and constraint_type != 'O')
loop
EXECUTE IMMEDIATE 'alter table _USER_.' ||i.table_name|| ' disable NOVALIDATE constraint ' ||i.constraint_name;
end loop i;
END;