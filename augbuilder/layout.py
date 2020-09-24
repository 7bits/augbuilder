def return_layout():
    """
    Returns layout.

    Returns:
        9 elements for transformation example 
    """
    return """
    <style>

    .main{
        overflow-x: hidden !important;
    }
    .main .block-container > div{

        width: 130% !important;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 2.5rem;
    }
    
    .main .element-container:nth-child(6),
    .main .element-container:nth-child(4),
    .main .element-container:nth-child(5){
        width: 30% !important;

    }

    .main .element-container:nth-child(1),
    .main .element-container:nth-child(2){
        width: 45% !important;
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
        width: 30% !important;
        height: 30% !important;
    }

    .main .stFileUploader > div,
    .main .stFileUploader > label{
        width: 98% !important;
    }
    .main .stImage {
        width: 40% !important;
        
    }

    .main .stImage > img{
        width: 100% !important;
        
    }
    </style>
    """
