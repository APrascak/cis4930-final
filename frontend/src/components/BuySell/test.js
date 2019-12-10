import React from 'react';


const Test = (props) => {
    return(      
    <h1>Passed props down  {props.amount}</h1>
    )
};
const condition = authUser => !!authUser;
export default (Test);