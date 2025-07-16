import {List, Datagrid, TextField} from "react-admin";

const ConstructorStandingsList = () => {
    return (
        <List>
            <Datagrid>
                <TextField source="constructor_name"></TextField>
                <TextField source="total_points"></TextField>
            </Datagrid>
        </List>);
}

export default ConstructorStandingsList;