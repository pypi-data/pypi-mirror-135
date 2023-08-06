BEGIN
for i IN (select table_name, constraint_name
from ALL_CONSTRAINTS
where status = 'DISABLED' and owner='_USER_'
and constraint_type!='R'
)
loop
EXECUTE IMMEDIATE 'alter table _USER_.' ||i.table_name|| ' enable novalidate constraint ' ||i.constraint_name;
end loop i;

for i IN (select table_name, constraint_name
from ALL_CONSTRAINTS
where constraint_type ='R' and owner='_USER_'
and status = 'DISABLED')
loop
EXECUTE IMMEDIATE 'alter table _USER_.' ||i.table_name|| ' enable novalidate constraint ' ||i.constraint_name;
end loop i;
END;