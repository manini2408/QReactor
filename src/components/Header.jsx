import { motion } from 'framer-motion';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  
  // Navigation links
  const links = [
    { title: 'Home', path: '/' },
    { title: 'About', path: '/about' },
    { title: 'Services', path: '/services' },
    { title: 'Contact', path: '/contact' }
  ];

  return (
    <header className="header">
      <motion.div 
        className="header__container"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
      >
        <motion.div 
          className="logo"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Link to="/">Your Brand</Link>
        </motion.div>
        
        <motion.nav className="desktop-nav">
          <ul>
            {links.map((link, i) => (
              <motion.li 
                key={link.title}
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * i, duration: 0.5 }}
                whileHover={{ y: -3 }}
              >
                <Link to={link.path}>{link.title}</Link>
              </motion.li>
            ))}
          </ul>
        </motion.nav>
        
        <motion.div 
          className="mobile-menu-button"
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsOpen(!isOpen)}
        >
          <div className={`hamburger ${isOpen ? 'open' : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </motion.div>
      </motion.div>
      
      {/* Mobile Menu */}
      <motion.div 
        className="mobile-menu"
        initial={{ height: 0, opacity: 0 }}
        animate={{ 
          height: isOpen ? 'auto' : 0, 
          opacity: isOpen ? 1 : 0 
        }}
        transition={{ duration: 0.3 }}
      >
        <motion.ul>
          {links.map((link, i) => (
            <motion.li 
              key={link.title}
              initial={{ opacity: 0, x: -10 }}
              animate={isOpen ? { opacity: 1, x: 0 } : { opacity: 0, x: -10 }}
              transition={{ delay: 0.05 * i, duration: 0.3 }}
              whileTap={{ scale: 0.95 }}
            >
              <Link to={link.path} onClick={() => setIsOpen(false)}>
                {link.title}
              </Link>
            </motion.li>
          ))}
        </motion.ul>
      </motion.div>
    </header>
  );
};

export default Header; 