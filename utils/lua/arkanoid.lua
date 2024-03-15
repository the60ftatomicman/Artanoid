s       = manager.machine.screens[":screen"]
cpu     = manager.machine.devices[":maincpu"]
mem     = cpu.spaces["program"]
SPEED = 0x06
function draw_hud()
	-- INFINITE LIVES
	mem:write_u8(0xED71,0x0F)
	
	-- MY attempts at SPEED control. setting C462 just makes it static.
	-- Adding the toggle was a mess that reset all the time
	-- if(manager.machine.input:code_pressed_once(manager.machine.input:code_from_token("KEYCODE_A")))then
	--	emu.print_info("change speed")
	--	if SPEED == 0x01 then
	--		SPEED = 0x06
	--	else
	-- SPEED = 0x01
	--	end
	-- mem:write_u8(0xC462,SPEED)
	--end
	
	-- Turn lasers on with S key. Dodge the thingy that falls!
	-- note if you adjust the integer at 0xc463 after this other pills will fall.
	-- following consecutive from 1-6 results in 6 becoming the break pill.
	if(manager.machine.input:code_pressed_once(manager.machine.input:code_from_token("KEYCODE_S")))then
		emu.print_info("LASERS")
		mem:write_u8(0xc463,0x01)
		mem:write_u8(0xC659,0x01)
	end
	-- Draw the text RED (0xffff0000) on BLACK (0xff000000)
	-- Format: 0xaarrggbb where a = alpha,
	s:draw_text(10, "LEFT", string.format("DOH mode"), 0xffff0000, 0xff000000);
end
emu.register_frame_done(draw_hud, "frame")