s    = manager.machine.screens[":screen"]
cpu  = manager.machine.devices[":maincpu"]
cpu2 = manager.machine.devices[":sub"]
mem  = cpu.spaces["program"]
mem2 = cpu2.spaces["program"]
function draw_hud()

	-- INFINITE LIVES
	mem:write_u8(0xE007,0x0F) 
	
	-- LASERS 1, LONG 2, twin 3/5,shield? 4,Catch 6, Ghost 7, 8 forgot....
	-- CRASHES 9
	-- NOTHING A,B,C,D,E,F
	mem:write_u8(0xE5EF,0x01)
	mem:write_u8(0xE5F0,0x01)
	
	-- Draw the text RED (0xffff0000) on BLACK (0xff000000)
	-- Format: 0xaarrggbb where a = alpha,
	s:draw_text(10, "LEFT", string.format("DOH MODE"), 0xffff0000, 0xff000000);
end
emu.register_frame_done(draw_hud, "frame")
mem2:write_u8(0x0A95,0xAF) -- This jumps past the checksum for the ROMS