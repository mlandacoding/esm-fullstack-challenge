import { Create, SimpleForm, TextInput } from "react-admin";

const DriverCreate = () =>{
    return (
        <Create>
            <SimpleForm>
                <TextInput source="driver_ref" label="Driver Ref" />
                <TextInput source="number" label="Number" />
                <TextInput source="code" label="Code" />
                <TextInput source="forename" label="Forename" />
                <TextInput source="surname" label="Surname" />
                <TextInput source="dob" label="Date of Birth" />
                <TextInput source="nationality" label="Nationality" />
                <TextInput source="url" label="URL" />
            </SimpleForm>
        </Create>
    );
}

export default DriverCreate;