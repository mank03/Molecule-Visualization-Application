/* javascript to accompany jquery.html */

$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {
      let pos = 'L';
  
      $("#p2").hide();  /* hide paragraph 2 */
  
      $("#b1").click(
        /* this defines a function that gets called after someone clicks 
         * the button */
        function()
        {
      $("#p2").toggle();
      $("#p1").toggle();
        } );
  
      $("#b2").click(
        /* function that gets called when button 2 is clicked */
        function()
        {
      $("#p3").fadeToggle(3000);
        } );
  
      $("#b3").mouseenter(
        function ()
        {
      if (pos=='L')
      {
        $("#b3").animate( {left: '250px'} );
        pos = 'R';
      }
      else
      {
        $("#b3").animate( {left: '0px'} );
        pos = 'L';
      }
        } );
  
      $("#b4").click(
        function()
        {
      alert( "Value:" + $("#element_code").val() );
        } );
  
      $("#b5").click(
        function()
        {
      $("#name").val("auto-fill");
        } );
  
      $("circle").click(
        function()
        {
      this.remove();
        } );
  
      $("#b6").click(
        function()
        {
      $("#svg_box").load( "solution.svg", alert( 'better?' ) );
        } );
    } );
  