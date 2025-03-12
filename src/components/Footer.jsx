import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.5, duration: 0.5 }}
    >
      <div className="footer-content">
        <div className="footer-columns">
          <motion.div 
            className="footer-column"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <h4>Company</h4>
            <ul>
              <motion.li whileHover={{ x: 5 }}>
                <Link to="/about">About Us</Link>
              </motion.li>
              <motion.li whileHover={{ x: 5 }}>
                <Link to="/team">Our Team</Link>
              </motion.li>
              <motion.li whileHover={{ x: 5 }}>
                <Link to="/careers">Careers</Link>
              </motion.li>
            </ul>
          </motion.div>
          
          <motion.div 
            className="footer-column"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <h4>Services</h4>
            <ul>
              <motion.li whileHover={{ x: 5 }}>
                <Link to="/services">All Services</Link>
              </motion.li>
              <motion.li whileHover={{ x: 5 }}>
                <Link to="/pricing">Pricing</Link>
              </motion.li>
              <motion.li whileHover={{ x: 5 }}>
                <Link to="/support">Support</Link>
              </motion.li>
            </ul>
          </motion.div>
          
          <motion.div 
            className="footer-column"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
          >
            <h4>Contact</h4>
            <ul>
              <motion.li whileHover={{ x: 5 }}>
                <Link to="/contact">Contact Us</Link>
              </motion.li>
              <motion.li whileHover={{ x: 5 }}>
                <a href="mailto:info@example.com">info@example.com</a>
              </motion.li>
              <motion.li whileHover={{ x: 5 }}>
                <a href="tel:+1234567890">+1 (234) 567-890</a>
              </motion.li>
            </ul>
          </motion.div>
        </div>
        
        <motion.div 
          className="footer-bottom"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.5 }}
        >
          <p>© {new Date().getFullYear()} Your Company. All rights reserved.</p>
          <div className="social-icons">
            {['twitter', 'facebook', 'instagram', 'linkedin'].map((social, i) => (
              <motion.a 
                key={social}
                href={`https://${social}.com`}
                target="_blank"
                rel="noopener noreferrer"
                whileHover={{ y: -3, scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
              >
                <i className={`icon-${social}`}></i>
              </motion.a>
            ))}
          </div>
        </motion.div>
      </div>
    </motion.footer>
  );
};

export default Footer; 