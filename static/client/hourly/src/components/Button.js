import React from "react";
import './Button.css'

/**
 * Represents a clickable, touchable interactive UI component.
 * @property label - represents the label to display on the button
 * @property onClick - represents the action taken on click
 * @property style - represents the extra styling
 * @constructor
 */
const Button = (props) => {

    return (
        <button className='btn-container' onClick={props.onClick} style={{...props.style}}>
            {props.label}
        </button>
    );
}

export default Button;