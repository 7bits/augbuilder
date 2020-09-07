def return_layout():
    """
    Returns layout.

    Returns:
        9 elements for transformation example 
    """
    return """
    <style>

    .main .block-container > div{

        width: 130% !important;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
    
    .main .element-container:nth-child(1),
    .main .element-container:nth-child(2){
        width: 50% !important;
    } 

    .main .element-container:nth-child(6),
    .main .element-container:nth-child(5){
        width: 0% !important;
    } 

   
    .main .element-container:nth-child(15),
    .main .element-container:nth-child(7),
    .main .element-container:nth-child(8),
    .main .element-container:nth-child(9),
    .main .element-container:nth-child(10),
    .main .element-container:nth-child(11),
    .main .element-container:nth-child(12),
    .main .element-container:nth-child(13),
     .main .element-container:nth-child(14){
        width: 33% !important;
        height: 33% !important;
    }
    
    .main .stFileUploader > div,
    .main .stFileUploader > label{
        width: 98% !important;
    }
    .main .stImage > img{
        width: 40% !important;
    }

    </style>
    """
