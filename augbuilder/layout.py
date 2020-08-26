def return_layout():

    return """
    <style>

    .main .block-container > div{

        width: 130% !important;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }
    
    .main .element-container:nth-child(3),
    .main .element-container:nth-child(4){
        width: 0% !important;
    } 

    .main .element-container:nth-child(5),
    .main .element-container:nth-child(6),
    .main .element-container:nth-child(7),
    .main .element-container:nth-child(8),
    .main .element-container:nth-child(9),
    .main .element-container:nth-child(10),
    .main .element-container:nth-child(11),
    .main .element-container:nth-child(12),
    .main .element-container:nth-child(13){
        width: 33% !important;
        height: 33% !important;
    }
    
    .main .stImage > img{
        width: 40% !important;
    }

    </style>
    """
